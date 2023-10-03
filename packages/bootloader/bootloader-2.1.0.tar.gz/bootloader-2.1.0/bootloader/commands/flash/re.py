from time import sleep

from cleo.helpers import argument
from semantic_version import Version

from bootloader.utilities.system_utils import run_command
from bootloader.utilities.system_utils import get_fw_file
from bootloader.utilities.help import re_help
from bootloader.utilities.system_utils import psoc_flash_command

from .base_flash import BaseFlashCommand


# ============================================
#              FlashReCommand
# ============================================
class FlashReCommand(BaseFlashCommand):
    name = "flash re"
    description = "Flashes new firmware onto Regulate."
    help = re_help()
    hidden = False

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        argument("to", "Version to flash, e.g., `9.1.0`, or path to file to use."),
        argument("rigidVersion", "PCB hardware version, e.g., `4.1B`."),
        argument("led", "Either 'mono', 'multi', or 'stealth'"),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._target = "re"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, version: Version) -> None:
        fName = f"{self._target}_version-{version}_"
        fName += f"rigid-{self._rigidVersion.lower()}_"
        fName += f"led-{self._led.lower()}color.cyacd"

        self._fwFile = get_fw_file(fName)

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = psoc_flash_command(
            self._port, self._fwFile, self.application._os
        )

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        sleep(3)
        self._device.close()
        run_command(self._flashCmd)
