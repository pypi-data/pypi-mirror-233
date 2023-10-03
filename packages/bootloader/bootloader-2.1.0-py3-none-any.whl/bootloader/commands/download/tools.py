from contextlib import suppress
import os
from pathlib import Path
import platform
import subprocess as sub
import sys
import zipfile

from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from flexsea.utilities.aws import s3_download
import flexsea.utilities.constants as fxc

import bootloader.utilities.constants as bc
from bootloader.utilities.help import tools_help
from bootloader.utilities.system_utils import run_command


# ============================================
#           DownloadToolsCommand
# ============================================
class DownloadToolsCommand(BaseCommand):
    name = "download tools"
    description = "Downloads the 3rd party tools needed to bootload the target."
    help = tools_help()
    hidden = False

    arguments = [
        argument("target", "The target to get tools for, e.g., mn, ex, or re."),
    ]

    # -----
    # handle
    # -----
    def handle(self) -> int:
        opSys = self.application._os

        self._search(opSys)
        if self.argument("target") == "setup":
            self._path_setup(opSys)
            if not bc.firstSetup.is_file():
                self._first_setup(opSys)

        self.line("")

        return 0

    # -----
    # _search
    # -----
    def _search(self, opSys: str) -> None:
        for tool in bc.bootloaderTools[opSys][self.argument("target")]:
            self.write(f"Searching for: <info>{tool}</info>...")

            dest = bc.toolsPath.joinpath(opSys, tool)

            if not dest.exists():
                self.line(f"\n\t<info>{tool}</info> <warning>not found.</warning>")
                self.write("\tDownloading...")
                dest.parent.mkdir(parents=True, exist_ok=True)

                toolObj = str(Path(bc.toolsDir).joinpath(opSys, tool).as_posix())
                s3_download(toolObj, fxc.dephyPublicFilesBucket, str(dest))

                if zipfile.is_zipfile(dest):
                    with zipfile.ZipFile(dest, "r") as archive:
                        base = dest.name.split(".")[0]
                        extractedDest = Path(os.path.dirname(dest)).joinpath(base)
                        archive.extractall(extractedDest)

                self.overwrite(f"\tDownloading... {self.application._SUCCESS}\n")

            else:
                msg = f"Searching for: <info>{tool}</info>..."
                msg += f"{self.application._SUCCESS}\n"
                self.overwrite(msg)

    # -----
    # _path_setup
    # -----
    def _path_setup(self, opSys: str) -> None:
        if "windows" in opSys:
            self._windows_path_setup(opSys)

    # -----
    # _windows_path_setup
    # -----
    def _windows_path_setup(self, opSys: str) -> None:
        dfusePath = str(
            bc.toolsPath.joinpath(opSys, "dfuse_command", "dfuse_v3.0.6", "Bin")
        )
        mingwPath = str(
            bc.toolsPath.joinpath(
                opSys,
                "mingw",
                "mingw-w64",
                "mingw-w64",
                "i686-8.1.0-posix-dwarf-rt_v6-rev0",
                "mingw32",
                "bin",
            )
        )
        stmFlashLoaderPath = str(
            bc.toolsPath.joinpath(
                opSys,
                "stm32_flash_loader",
                "stm32_flash_loader",
            )
        )
        os.environ["PATH"] += os.pathsep + dfusePath
        os.environ["PATH"] += os.pathsep + mingwPath
        os.environ["PATH"] += os.pathsep + stmFlashLoaderPath

    # -----
    # _first_setup
    # -----
    def _first_setup(self, opSys: str) -> None:
        if "windows" in opSys:
            self._install_st_drivers(opSys)
            self._install_dfuse_drivers(opSys)

    # -----
    # _install_st_drivers
    # -----
    def _install_st_drivers(self, opSys: str) -> None:
        msg = "We're about to install ST Link. At the end of the installation "
        msg += "process, a window will pop up asking you to install the STM "
        msg += "drivers. <warning>You MUST install these or bootloading will "
        msg += "not work.</warning>"
        self.line(msg)
        # There's a bug in cleo where, when calling one command from another, if
        # the command being called uses `confirm`, then _stream isn't set, which
        # causes a no attribute error: https://github.com/python-poetry/cleo/issues/333
        # As a workaround, we make it not interactive or don't use confirm
        proceed = input("Proceed? [y/n]")
        if proceed.lower() != "y":
            self.line("Acknowledgment to install drivers not given. Aborting.")
            sys.exit(1)
        cmd = [
            str(bc.toolsPath.joinpath(opSys, "stlink_setup.exe")),
        ]
        try:
            run_command(cmd)
        except (RuntimeError, sub.TimeoutExpired):
            self.line("Error: could not install STM drivers.")
            sys.exit(1)

    # -----
    # _install_dfuse_drivers
    # -----
    def _install_dfuse_drivers(self, opSys: str) -> None:
        # There's a bug in cleo where, when calling one command from another, if
        # the command being called uses `confirm`, then _stream isn't set, which
        # causes a no attribute error: https://github.com/python-poetry/cleo/issues/333
        # As a workaround, we make it not interactive or don't use confirm
        proceed = input("We're about to install the DfuSe drivers. Proceed? [y/n]")
        if proceed.lower() != "y":
            self.line("Acknowledgment to install drivers not given. Aborting.")
            sys.exit(1)
        winRelease = platform.release()
        try:
            assert winRelease in bc.supportedWindowsVersions
        except AssertionError:
            msg = "Error: unsupported Windows version. Must be using one of the "
            msg += f"following Windows versions: {bc.supportedWindowsVersions}"
            self.line(msg)
            sys.exit(1)
        # There is no windows 11 specific installer, but the windows 10
        # installer appears to work
        if winRelease == "11":
            winRelease = "10"
        if "64bit" in opSys:
            installer = "dpinst_amd64.exe"
        else:
            installer = "dpinst_x86.exe"
        cmd = [
            str(
                bc.toolsPath.joinpath(
                    opSys,
                    "dfuse_command",
                    "dfuse_v3.0.6",
                    "Bin",
                    "Driver",
                    f"Win{winRelease}",
                    f"{installer}",
                )
            ),
        ]
        # For some reason, the dpinst executable returns a non-zero exit
        # code even when the drivers install successfully. This causes
        # run_command to error out, so we call the executable directly
        with suppress(sub.CalledProcessError):
            _ = sub.run(cmd, capture_output=False, check=True, timeout=360)
        bc.firstSetup.touch()
