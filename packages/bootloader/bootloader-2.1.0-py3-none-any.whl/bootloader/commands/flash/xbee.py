import os
from time import sleep

from cleo.helpers import argument
from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.help import xbee_help
from bootloader.utilities.system_utils import run_command

from .base_flash import BaseFlashCommand


# ============================================
#              FlashXbeeCommand
# ============================================
class FlashXbeeCommand(BaseFlashCommand):
    name = "flash xbee"
    description = "Flashes new firmware onto Xbee."
    help = xbee_help()
    hidden = False

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        argument("address", "Bluetooth address."),
        argument("buddyAddress", "Bluetooth address of device's buddy."),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._target = "xbee"

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Xbee doesn't need a firmware file.
        """

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        if "windows" in self.application._os:
            pythonCmd = "python"
        else:
            pythonCmd = "python3"

        address = self._address if self._address else self._device.id

        self._flashCmd = [
            pythonCmd,
            os.path.join(
                bc.toolsPath, self.application._os, "XB24C", "XB24C", "xb24c.py"
            ),
            self._port,
            str(address),
            self._buddyAddress,
            "upgrade",
        ]

    # -----
    # _flash_target
    # -----
    def _flash_target(self) -> None:
        self._device.close()
        sleep(3)
        run_command(self._flashCmd)
        sleep(20)

    # -----
    # _handle_firmware_version
    # -----
    def _handle_firmware_version(self, version: Version) -> None:
        raise NotImplementedError
