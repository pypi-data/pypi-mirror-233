from cleo.commands.command import Command as BaseCommand


# ============================================
#                 LogoCommand
# ============================================
class LogoCommand(BaseCommand):
    name = "logo"
    description = "Shows Dephy logo."
    help = "Shows Dephy logo."
    hidden = True

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Prints Dephy logo.
        """
        logo = """
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
        ██░▄▄▀██░▄▄▄██░▄▄░██░██░██░███░██
        ██░██░██░▄▄▄██░▀▀░██░▄▄░██▄▀▀▀▄██
        ██░▀▀░██░▀▀▀██░█████░██░████░████
        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n\t          Beyond Nature™
        """
        self.line("")
        self.line("")
        try:
            self.line(logo)
        except UnicodeEncodeError:
            self.line("Dephy\nBeyond Nature (TM)")

        return 0
