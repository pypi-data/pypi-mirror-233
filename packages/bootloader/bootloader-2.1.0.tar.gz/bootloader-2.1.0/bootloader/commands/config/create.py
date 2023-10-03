from pathlib import Path
import sys
import tempfile
from zipfile import ZipFile

from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from cleo.helpers import option
from flexsea.utilities.firmware import validate_given_firmware_version
import pendulum
import yaml

import bootloader.utilities.constants as bc
from bootloader.utilities.help import config_create_help


# ============================================
#           ConfigCreateCommand
# ============================================
class ConfigCreateCommand(BaseCommand):
    name = "config create"
    description = "Creates a collection of files that can be flashed via `flash config`"
    help = config_create_help()

    arguments = [argument("configName", "Name of the configuration.")]

    options = [
        option("mn-file", None, "File to use for Manage.", flag=False),
        option("ex-file", None, "File to use for Execute.", flag=False),
        option("re-file", None, "File to use for Regulate.", flag=False),
        option("habs-file", None, "File to use for Habsolute.", flag=False),
        option("firmware-version", None, "Version of C library to use.", flag=False),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._mnFile: str = ""
        self._exFile: str = ""
        self._reFile: str = ""
        self._habsFile: str = ""
        self._firmwareVersion: str = ""
        self._libFile: str = ""
        self._configName: str = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self._configName = self.argument("configName")
        archiveName = self._get_archive_name()
        files = self._get_files()
        files["infoFile"] = self._get_info_file(files)

        with ZipFile(archiveName, "w") as archive:
            for value in files.values():
                archive.write(value["path"], arcname=value["arcname"])

        self._print_summary(files)

        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("config upload", f"PLACEHOLDER {archiveName}")

        return 0

    # -----
    # _get_archive_name
    # -----
    def _get_archive_name(self) -> str:
        archiveName = f"{self._configName}.zip"

        # Check for existing local archive
        if Path(archiveName).resolve().is_file():
            if not self.confirm(
                f"Archive {archiveName} already exists. Overwrite?", False
            ):
                self.line("Aborting.")
                sys.exit(1)

        # Make sure no archive with this name exists on S3
        with tempfile.NamedTemporaryFile("w+") as fd:
            # We can change the stream cleo writes to by accessing the _stream
            # directly. This allows us to capture the output of a command in a
            # file and then read that file to inspect the output. There's
            # probably a cleaner way of doing this, but I don't know what it is
            # The only potential issue is if something goes wrong in show configs,
            # I need to set the stream back to stdout, otherwise the error messages
            # will be suppressed. NOTE: contextlib.redirect_stdout doesn't seem to
            # work
            self.io.output._stream = fd
            self.call("show configs")
            self.io.output._stream = sys.stdout
            fd.seek(0)
            availableConfigs = fd.read()
            if archiveName in availableConfigs:
                raise RuntimeError(f"Error: {archiveName} already exists on S3.")
        return archiveName

    # -----
    # _get_files
    # -----
    def _get_files(self) -> dict:
        files = {}
        nFiles = 0

        for target in ["mn", "ex", "re", "habs"]:
            if self.option(f"{target}-file"):
                fPath = Path(self.option(f"{target}-file")).expanduser().resolve()
            else:
                fName = self.ask(
                    f"Enter a file for {target} (leave blank to skip):", None
                )
                if fName is None:
                    continue
                fPath = Path(fName).expanduser().resolve()
            try:
                assert fPath.is_file()
            except AssertionError as err:
                raise FileNotFoundError(f"Error: could not find {fPath}") from err
            # We use a str for path because yaml can't write a Path
            # We use arcname so that the zip structure is flat
            files[target] = {"path": str(fPath), "arcname": fPath.name}
            nFiles += 1

        # Make sure the user didn't skip everything
        try:
            assert nFiles > 0
        except AssertionError as err:
            raise RuntimeError(
                "Error: need at least one file to create a configuration"
            ) from err

        return files

    # -----
    # _get_firmware_version
    # -----
    def _get_firmware_version(self) -> str:
        if self.option("firmware-version"):
            fwVer = self.option("firmware-version")
        else:
            fwVer = self.ask(
                "Which firmware version is this configuration associated with: ", None
            )

        return str(validate_given_firmware_version(fwVer, True))

    # -----
    # _get_info_file
    # -----
    def _get_info_file(self, files: dict) -> dict:
        """
        Writes meta-data about the configuration (such as firmware version)
        to a file that gets included in the archive.
        """
        info = {k: files[k]["arcname"] for k in files}
        info["date"] = str(pendulum.today())
        info["firmware_version"] = self._get_firmware_version()
        with open(bc.configInfoFile, "w", encoding="utf8") as fd:
            yaml.safe_dump(info, fd)

        return {"path": bc.configInfoFile, "arcname": bc.configInfoFile}

    # -----
    # _print_summary
    # -----
    def _print_summary(self, files: dict) -> None:
        self.line("Configuration Summary")
        self.line("---------------------")
        self.line(f"* Configuration name: {self._configName}")
        for target in files:
            self.line(f"* {target} file: {files[target]['path']}")
        if not self.confirm("Proceed?", False):
            self.line("Aborting.")
            sys.exit(1)
