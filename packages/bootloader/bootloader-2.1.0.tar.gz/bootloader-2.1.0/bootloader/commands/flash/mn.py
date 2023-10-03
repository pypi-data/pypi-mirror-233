from pathlib import Path
from time import sleep

from cleo.helpers import argument
from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.help import mn_help
from bootloader.utilities.system_utils import run_command
from bootloader.utilities.system_utils import get_fw_file

from .base_flash import BaseFlashCommand


# ============================================
#              FlashMnCommand
# ============================================
class FlashMnCommand(BaseFlashCommand):
    name = "flash mn"
    description = "Flashes new firmware onto Manage."
    help = mn_help()
    hidden = False

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        argument("to", "Version to flash, e.g., `9.1.0`, or path to file to use."),
        argument("rigidVersion", "PCB hardware version, e.g., `4.1B`."),
        argument("deviceName", "Name of the device, e.g., actpack."),
        argument("side", "left, right, or none."),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._target = "mn"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, version: Version) -> None:
        fName = f"{self._target}_version-{version}_"
        fName += f"device-{self._deviceName.lower()}_"
        fName += f"rigid-{self._rigidVersion.lower()}_"
        fName += f"side-{self._side.lower()}.dfu"

        self._fwFile = get_fw_file(fName)

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            f"{Path(bc.toolsPath).joinpath(self.application._os, 'DfuSeCommand.exe')}",
            "-c",
            "-d",
            "--fn",
            f"{self._fwFile}",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        del self._device
        sleep(3)
        sleep(10)
        run_command(self._flashCmd)
