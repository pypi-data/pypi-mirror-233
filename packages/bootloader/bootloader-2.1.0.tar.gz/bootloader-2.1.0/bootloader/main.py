from .application import Application


# ============================================
#                    main
# ============================================
def main() -> None:
    """
    Entry point. Creates an instance of the command-line interface (CLI)
    and runs it.
    """
    Application().run()
