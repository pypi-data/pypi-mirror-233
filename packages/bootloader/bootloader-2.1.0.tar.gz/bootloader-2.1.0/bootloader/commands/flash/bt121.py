import glob
import os
import shutil
import subprocess as sub
from time import sleep

from cleo.helpers import argument
from semantic_version import Version

import bootloader.utilities.constants as bc
from bootloader.utilities.help import bt121_help
from bootloader.utilities.system_utils import run_command

from .base_flash import BaseFlashCommand


# ============================================
#              FlashBt121Command
# ============================================
class FlashBt121Command(BaseFlashCommand):
    name = "flash bt121"
    description = "Flashes new firmware onto Bt121."
    help = bt121_help()
    hidden = False

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
        argument("address", "Bluetooth address."),
        argument("level", "Gatt level to use."),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._target = "bt121"

    # -----
    # _get_firmware_file
    # -----
    def _get_firmware_file(self) -> None:
        """
        Uses the bluetooth tools repo to create a bluetooth image file
        with the correct address.
        """
        self.line("")
        self.line("Building bluetooth image...")

        address = self._address if self._address else self._device.id

        # Everything within the bt121 directory is self-contained and
        # self-referencing, so it's easiest to switch to that directory
        # first
        cwd = os.getcwd()
        # The way the zip is decompressed creates this nested structure
        os.chdir(
            os.path.join(
                bc.toolsPath,
                self.application._os,
                "bt121_image_tools",
                "bt121_image_tools",
            )
        )

        gattTemplate = os.path.join("gatt_files", f"LVL{self._level}.xml")
        gattFile = os.path.join("dephy_gatt_broadcast_bt121", "gatt.xml")

        if not os.path.exists(gattTemplate):
            raise FileNotFoundError(f"Could not find: `{gattTemplate}`.")

        shutil.copyfile(gattTemplate, gattFile)

        if "linux" in self.application._os:
            pythonCommand = "python3"
        elif "windows" in self.application._os:
            pythonCommand = "python"
        else:
            raise OSError("Unsupported OS!")

        cmd = [pythonCommand, "bt121_gatt_broadcast_img.py", f"{address}"]
        proc = sub.run(cmd, capture_output=False, check=True, timeout=360)

        if proc.returncode != 0:
            raise RuntimeError("bt121_gatt_broadcast_img.py failed.")

        bgExe = os.path.join("smart-ready-1.7.0-217", "bin", "bgbuild.exe")
        xmlFile = os.path.join("dephy_gatt_broadcast_bt121", "project.xml")
        proc = sub.run([bgExe, xmlFile], capture_output=False, check=True, timeout=360)

        if proc.returncode != 0:
            raise RuntimeError("bgbuild.exe failed.")

        if os.path.exists("output"):
            files = glob.glob(os.path.join("output", "*.bin"))
            for file in files:
                os.remove(file)
        else:
            os.mkdir("output")

        btImageFile = f"dephy_gatt_broadcast_bt121_Exo-{self._address}.bin"
        shutil.move(os.path.join("dephy_gatt_broadcast_bt121", btImageFile), "output")
        btImageFile = os.path.join(os.getcwd(), "output", btImageFile)

        os.chdir(cwd)

        self._fwFile = btImageFile
        self.line(f"Building bluetooth image... {self.application._SUCCESS}")

    # -----
    # _get_flash_command
    # -----
    def _get_flash_command(self) -> None:
        self._flashCmd = [
            str(bc.toolsPath.joinpath(self.application._os, "stm32flash")),
            "-w",
            f"{self._fwFile}",
            "-b",
            "115200",
            self._device.port,
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
