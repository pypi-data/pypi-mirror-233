import bootloader.utilities.constants as bc
from bootloader.utilities.help import show_rigids_help

from .base_show import BaseShowCommand


# ============================================
#             ShowRigidsCommand
# ============================================
class ShowRigidsCommand(BaseShowCommand):
    name = "show rigids"
    description = "Lists all rigid versions for which there is firmware."
    help = show_rigids_help()

    # -----
    # handle
    # -----
    def handle(self) -> int:
        rigids = set()
        firmwarePath = self._get_cloud_path(bc.dephyFirmwareBucket)

        for fwPath in firmwarePath.iterdir():
            fwFile = fwPath.name
            # All rigid names are only present in the re file names
            if not fwFile.startswith("re_"):
                continue
            rigids.add(fwFile.split("_")[2].split("-")[1])

        self.line("")
        self.line("Available Rigid Versions")
        self.line("------------------------")

        for version in sorted(list(rigids)):
            self.line(f"* {version}")

        self.line("")

        return 0
