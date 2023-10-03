import bootloader.utilities.constants as bc
from bootloader.utilities.help import show_devices_help

from .base_show import BaseShowCommand


# ============================================
#            ShowDevicesCommand
# ============================================
class ShowDevicesCommand(BaseShowCommand):
    name = "show devices"
    description = "Lists all devices for which there is firmware."
    help = show_devices_help()

    # -----
    # handle
    # -----
    def handle(self) -> int:
        devices = set()
        firmwarePath = self._get_cloud_path(bc.dephyFirmwareBucket)

        for fwPath in firmwarePath.iterdir():
            fwFile = fwPath.name
            # The device names are only present in the mn file names
            if not fwFile.startswith("mn_"):
                continue
            devices.add(fwFile.split("_")[2].split("-")[1])

        self.line("")
        self.line("Available Devices")
        self.line("-----------------")

        for device in sorted(list(devices)):
            self.line(f"* {device}")

        self.line("")

        return 0
