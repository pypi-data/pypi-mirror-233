from pathlib import Path
import re
from time import sleep

from cleo.helpers import argument
from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.help import habs_help
from bootloader.utilities.system_utils import run_command
from bootloader.utilities.system_utils import get_fw_file

from .base_flash import BaseFlashCommand


# ============================================
#              FlashHabsCommand
# ============================================
class FlashHabsCommand(BaseFlashCommand):
    name = "flash habs"
    description = "Flashes new firmware onto Habsolute."
    help = habs_help()
    hidden = False

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        argument("to", "Version to flash, e.g., `9.1.0`, or path to file to use."),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._target = "habs"

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, version: Version) -> None:
        fName = f"{self._target}_version-{version}.hex"
        self._fwFile = get_fw_file(fName)

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        cmd = Path.joinpath(
            bc.toolsPath,
            self.application._os,
            "stm32_flash_loader",
            "stm32_flash_loader",
            "STMFlashLoader.exe",
        )
        portNum = re.search(r"\d+$", self._port).group(0)

        self._flashCmd = [
            f"{cmd}",
            "-c",
            "--pn",
            f"{portNum}",
            "--br",
            "115200",
            "--db",
            "8",
            "--pr",
            "NONE",
            "-i",
            "STM32F3_7x_8x_256K",
            "-e",
            "--all",
            "-d",
            "--fn",
            f"{self._fwFile}",
            "-o",
            "--set",
            "--vals",
            "--User",
            "0xF00F",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(6)
        run_command(self._flashCmd)
        sleep(20)
