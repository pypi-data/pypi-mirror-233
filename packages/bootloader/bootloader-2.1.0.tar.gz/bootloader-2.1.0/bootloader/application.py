from contextlib import suppress
from importlib import import_module
import sys

from cleo.application import Application as BaseApplication
from cleo.exceptions import CleoError
from cleo.formatters.style import Style
from cleo.helpers import option
from cleo.io.io import IO
from flexsea.utilities.system import get_os

from bootloader import __version__
import bootloader.exceptions.exceptions as bex
from bootloader.command_list import COMMANDS
import bootloader.utilities.constants as bc
from bootloader.utilities.system_utils import setup_cache


# ============================================
#                 Application
# ============================================
class Application(BaseApplication):
    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__("bootloader", __version__)

        self._os = get_os()

        if sys.stdout.encoding.lower().startswith("utf"):  # pylint: disable=no-member
            self._SUCCESS = "<success>✓</success>"
        else:
            self._SUCCESS = "SUCCESS"

        self._load_commands()

        setup_cache()

    # -----
    # _load_commands
    # -----
    def _load_commands(self) -> None:
        """
        This saves us from having to import lots of classes. The names
        of the commands match the names of the files, and by nesting
        directories in the `commands` directory we can have multi-word
        commands. E.g., `commands/env/create.py` would be the command
        `bootload env create`. The name in `COMMANDS` would be
        'env create'.
        """
        for name in COMMANDS:
            words = name.split(" ")
            module = import_module("bootloader.commands." + ".".join(words))
            cmdClass = getattr(module, "".join(c.title() for c in words) + "Command")
            command = cmdClass()
            self.add(command)

    # -----
    # _default_definition
    # -----
    @property
    def _default_definition(self):
        """
        This is an override of cleo's method. It's where
        application-level options such as `--quiet` and `--verbose`
        are set. Here we override it in order to add the `--theme`
        option so each command does not need to be configured
        individually.
        """
        definition = super()._default_definition
        themeOpt = option("--theme", "-t", "Sets theme.", flag=False)
        debugOpt = option("--debug", None, "Enables tracebacks.", flag=True)
        definition.add_option(themeOpt)
        definition.add_option(debugOpt)
        return definition

    # -----
    # _configure_io
    # -----
    def _configure_io(self, io: IO) -> None:
        """
        Whenever a command's `run` method is called, cleo calls
        `_create_io` and `_configure_io`. Here we override
        `configure_io` to be able to configure the theme of each
        command.
        """
        # This is for multi-word commands, e.g., flash mn, because at this
        # point that hasn't been configured
        with suppress(CleoError):
            # This actually parses the command-line to give each option a
            # value
            io.input.bind(self.definition)

        theme = io.input.option("theme")
        try:
            assert theme in bc.themes
        except AssertionError:
            theme = "default"

        formatter = io.output.formatter

        for styleName, styleOpts in bc.themes[theme].items():
            formatter.set_style(styleName, Style(**styleOpts))

        io.output.set_formatter(formatter)
        io.error_output.set_formatter(formatter)

        if not io.is_interactive() and not io.input.option("no-interaction"):
            io.interactive(True)

        if not io.input.option("debug"):
            sys.tracebacklimit = 0

        super()._configure_io(io)

    # -----
    # _run
    # -----
    def _run(self, io: IO) -> int:
        if self._os not in bc.supportedOS:
            raise bex.UnsupportedOSError(self._os)

        return super()._run(io)
