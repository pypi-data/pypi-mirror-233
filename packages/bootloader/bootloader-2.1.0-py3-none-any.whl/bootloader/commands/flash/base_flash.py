from pathlib import Path
import sys
from typing import List

from cleo.commands.command import Command as BaseCommand
from cleo.helpers import option
from flexsea.device import Device
from flexsea.utilities.firmware import validate_given_firmware_version
from semantic_version import Version

import bootloader.utilities.constants as bc


# ============================================
#              BaseFlashCommand
# ============================================
class BaseFlashCommand(BaseCommand):
    """
    The overall process for flashing each target is the same; the
    differences lie in the required arguments, the third-party tool
    used for actually doing the flashing, and the sleeps involved.

    The goal of this object is to encapsulate the overall process,
    leaving the minor differences to the target-specific commands.
    """

    options = [
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("libFile", "-l", "C lib for interacting with Manage.", flag=False),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._address: str = ""
        self._baudRate: int = 0
        self._buddyAddress: str = ""
        self._currentMnFw: str = ""
        self._device: Device | None = None
        self._deviceName: str = ""
        self._flashCmd: List[str] | None = None
        self._fwFile: Path | str | None = None
        self._led: str = ""
        self._level: str = ""
        self._libFile: str = ""
        self._motorType: str = ""
        self._port: str = ""
        self._rigidVersion: str = ""
        self._side: str = ""
        self._target: str = ""
        self._to: str = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Entry point for the command.

        Once we've parsed the given command-line arguments and options,
        we need to:

        * Check if the flash tool(s) required by the target are
            installed and download them if they aren't
        * Obtain the firmware file to be flashed. If we're given a
            file, we make sure the file exists and that it is
            the correct type for the target. If we're given a
            version number, we check to see if the file exists and,
            if not, download it from S3
        * Connect to the device
        * Build the command that will run the third-party flash
            tool
        * Provide a summary to the user and ask for their final
            confirmation
        * Put the device into tunnel mode
        * Call the aforementioned flash command
        """
        self.call("logo")
        self._parse_command_line()
        self._sanitize_command_line_values()
        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("download tools", "PLACEHOLDER setup")
        self.call("download tools", f"PLACEHOLDER {self._target}")
        self._get_firmware_file()
        self._get_device()
        self._get_flash_command()
        self._confirm()
        self._set_tunnel_mode()
        self._flash()

        return 0

    # -----
    # _parse_command_line
    # -----
    def _parse_command_line(self) -> None:
        """
        Stores each command-line argument and option in a hidden
        attribute of the same name for ease of access.
        """
        for arg in self.arguments:
            if hasattr(self, f"_{arg.name}"):
                setattr(self, f"_{arg.name}", self.argument(arg.name))
        for opt in self.options:
            if hasattr(self, f"_{opt.name}"):
                setattr(self, f"_{opt.name}", self.option(opt.name))

    # -----
    # _sanitize_command_line_values
    # -----
    def _sanitize_command_line_values(self) -> None:
        """
        Owing to how firmware files were originally built and named,
        there are some quirks that we iron out here to make the names
        easier to work with. This allows the files to be stored in
        their original form on S3 (so no other tooling breaks) and not
        need duplicate files.
        """
        # The mn and ex filenames don't have B in them for rigid 4.1B,
        # since they're the same file for rigid 4.1 and 4.1B. In order
        # to avoid having duplicate files with different names on S3,
        # we just handle it here
        if self._target in ["mn", "ex"]:
            if self._rigidVersion.lower().endswith("b"):
                self._rigidVersion = self._rigidVersion.lower().rstrip("b")

        # Ex filenames don't differentiate between rigid 4.1 and 4.0, so
        # for the same reasons as above, there is only a 4.0 file, so we
        # convert it here
        if self._target == "ex":
            if self._rigidVersion == "4.1":
                self._rigidVersion = "4.0"

    # -----
    # _get_device
    # -----
    def _get_device(self) -> None:
        """
        Creates an instance of the `Device` class and opens it.
        """
        self.line("")
        self.write("Connecting to device...")

        self._device = Device(
            self._currentMnFw,
            self._port,
            baudRate=int(self._baudRate),
            libFile=self._libFile,
            interactive=not self.option("no-interaction"),
        )

        # No idea why pylint complains about the bootloading keyword here. bootloader
        # requires >=v11.0.9 for flexsea, which has the keyword in open
        # pylint: disable-next=unexpected-keyword-arg
        self._device.open(bootloading=True)

        self.overwrite(f"Connecting to device... {self.application._SUCCESS}")
        self.line("")

    # -----
    # _set_tunnel_mode
    # -----
    def _set_tunnel_mode(self) -> None:
        """
        Puts Manage into tunnel mode so that we can communicate to the
        desired target through Manage.
        """
        self.line("")
        if not self.option("no-interaction"):
            msg = "<warning>Please make sure the battery is removed "
            msg += "and/or the power supply is disconnected!</warning>"

            if not self.confirm(msg, False):
                sys.exit(1)

        self.line("")
        self.write(f"Setting tunnel mode for {self._target}...")

        if not self._device.set_tunnel_mode(self._target, 20):
            self.line("")
            msg = "\n<error>Error</error>: failed to activate bootloader for: "
            msg += f"<warning>`{self._target}`</warning>"
            self.line(msg)
            sys.exit(1)

        msg = f"Setting tunnel mode for {self._target}... {self.application._SUCCESS}"
        self.overwrite(msg)
        self.line("")

    # -----
    # _flash
    # -----
    def _flash(self) -> None:
        """
        Calls the appropriate executable for flashing the desired target.
        """
        self.line("")
        self.write(f"Flashing {self._target}...")

        self._flash_target()

        self.overwrite(f"Flashing {self._target}... {self.application._SUCCESS}")
        self.line("")

        # There's a bug in cleo where, when calling one command from another, if
        # the command being called uses `confirm`, then _stream isn't set, which
        # causes a no attribute error: https://github.com/python-poetry/cleo/issues/333
        # As a workaround, we make it not interactive or don't use confirm
        # Here, though, we always want to prompt so that the user knows to power-cycle
        userInput = input(
            "Please power cycle the device. Press 'c' when done to continue."
        )
        if userInput.lower() != "c":
            sys.exit(1)

        self.line("")

    # -----
    # _confirm
    # -----
    def _confirm(self) -> None:
        self.line("")
        self.line("SUMMARY")
        self.line("-------")

        for arg in self.arguments:
            if hasattr(self, f"_{arg.name}") and getattr(self, f"_{arg.name}"):
                self.line(f"* {arg.name} : {getattr(self, '_' + arg.name)}")
        for opt in self.options:
            if hasattr(self, f"_{opt.name}") and getattr(self, f"_{opt.name}"):
                self.line(f"* {opt.name} : {getattr(self, '_' + opt.name)}")

        if not self.option("no-interaction"):
            if not self.confirm("Proceed?"):
                self.line("<error>Aborting.</>")
                sys.exit(1)

        self.line("")

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Checks to see if the user gave us a semantic version string or
        a file name for self.argument("to"). Then calls the appropriate
        handler methods.
        """
        # If self._to is a file instead of a version string,
        # validate_given_firmware_version raises a ValueError
        try:
            desiredFirmwareVersion = validate_given_firmware_version(
                self._to, not self.option("no-interaction")
            )
        except ValueError:
            self._handle_firmware_file()
        else:
            self._handle_firmware_version(desiredFirmwareVersion)

    # -----
    # _handle_firmware_file
    # -----
    def _handle_firmware_file(self) -> None:
        """
        Checks to make sure the given file both exists and has the
        correct file extension expected for the given target.
        """
        self._fwFile = Path(self._to).expanduser().resolve()
        if not self._fwFile.is_file():
            raise RuntimeError(f"Error: could not find given firmware file: {self._to}")
        if not self._fwFile.name.endswith(bc.firmwareExtensions[self._target]):
            msg = f"Invalid file extension for {self._target}. "
            msg += f"Expected {bc.firmwareExtensions[self._target]}."
            raise RuntimeError(msg)

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, version: Version) -> None:
        """
        If the user gave a semantic version string for
        self.argument("to"), then we have to build up the name of the
        firmware file to use based on the other arguments passed on
        the command line, and that is target-specific.
        """
        raise NotImplementedError

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        """
        Constructs the shell command needed to flash the given target,
        which is target-dependent.
        """
        raise NotImplementedError

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        """
        Each target has its own set of sleeps and operations related
        to closing the serial port that need to be performed before
        the flash command can be called, and this is target-specific.
        """
        raise NotImplementedError
