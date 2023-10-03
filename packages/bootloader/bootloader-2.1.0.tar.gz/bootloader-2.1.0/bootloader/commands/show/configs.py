import bootloader.utilities.constants as bc
from bootloader.utilities.help import show_configs_help

from .base_show import BaseShowCommand


# ============================================
#              ShowConfigsCommand
# ============================================
class ShowConfigsCommand(BaseShowCommand):
    name = "show configs"
    description = "Displays the available pre-made configurations for flashing."
    help = show_configs_help()

    # -----
    # handle
    # -----
    def handle(self) -> int:
        configsPath = self._get_cloud_path(bc.dephyConfigsBucket)

        self.line("")
        self.line("Available Configurations")
        self.line("------------------------")

        for config in configsPath.iterdir():
            self.line(f"* {config.name.split('.zip')[0]}")

        self.line("")
        self.line("\nTo use a configuration: `bootloader flash config <config name>`")

        return 0
