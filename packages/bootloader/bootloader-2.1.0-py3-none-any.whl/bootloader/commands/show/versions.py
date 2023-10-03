import bootloader.utilities.constants as bc
from bootloader.utilities.help import show_versions_help

from .base_show import BaseShowCommand


# ============================================
#             ShowVersionsCommand
# ============================================
class ShowVersionsCommand(BaseShowCommand):
    name = "show versions"
    description = "Lists all available firmware versions."
    help = show_versions_help()

    # -----
    # handle
    # -----
    def handle(self) -> int:
        versions = set()
        firmwarePath = self._get_cloud_path(bc.dephyFirmwareBucket)

        for fwPath in firmwarePath.iterdir():
            fwFile = fwPath.name
            # Can get the version from any file, but we'll use mn
            if not fwFile.startswith("mn_"):
                continue
            versions.add(fwFile.split("_")[1].split("-")[1])

        self.line("")
        self.line("Available Firmware Versions")
        self.line("---------------------------")

        for version in sorted(list(versions)):
            self.line(f"* {version}")

        self.line("")

        return 0
