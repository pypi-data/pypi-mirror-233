from typing import List

from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from cleo.helpers import option

from bootloader.utilities.help import all_help


# ============================================
#              FlashAllCommand
# ============================================
class FlashAllCommand(BaseCommand):
    name = "flash all"
    description = "Flashes new firmware onto xbee, bt121, habs, ex, re, and mn."
    help = all_help()
    hidden = False

    arguments = [
        argument("port", "Port the device is on, e.g., `COM3`."),
        argument("currentMnFw", "Manage's current firmware, e.g., `7.2.0`."),
    ]

    options = [
        option("to", "Version to flash, e.g., `9.1.0`, or path to file to use."),
        option("rigidVersion", "PCB hardware version, e.g., `4.1B`."),
        option("device", "Name of the device, e.g., actpack."),
        option("side", "left, right, or none."),
        option("motorType", "Either 'actpack', 'exo', or '61or91'"),
        option("led", "Either 'mono', 'multi', or 'stealth'"),
        option("address", "Bluetooth address."),
        option("level", "Gatt level to use."),
        option("buddyAddress", "Bluetooth address of device's buddy."),
        option("baudRate", "-b", "Device baud rate.", flag=False, default=230400),
        option("libFile", "-l", "C lib for interacting with Manage.", flag=False),
    ]

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self._argList: str = ""
        self._optList: str = ""

    # -----
    # handle
    # -----
    def handle(self) -> int:
        # Handle the args and opts passed to every command
        self._argList = f"{self.argument('port')} {self.argument('currentMnFw')} "

        if self.option("baudRate"):
            self._optList += f"--baudRate {self.option('baudRate')} "
        if self.option("libFile"):
            self._optList += f"--libFile {self.option('libFile')} "

        self._flash_xbee()
        self._flash_bt121()
        self._flash_habs()
        self._flash_ex()
        self._flash_re()
        self._flash_mn()

        return 0

    # -----
    # _flash_xbee
    # -----
    def _flash_xbee(self) -> None:
        self.line("")

        if not self.confirm("Flash xbee?"):
            return
        args = self._get_arg_list(["address", "buddyAddress"])
        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("flash xbee", f"PLACEHOLDER {args} {self._optList} --no-interaction")

        self.line("")

    # -----
    # _flash_bt121
    # -----
    def _flash_bt121(self) -> None:
        self.line("")

        if not self.confirm("Flash bt121?"):
            return
        args = self._get_arg_list(["address", "level"])
        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("flash bt121", f"PLACEHOLDER {args} {self._optList} --no-interaction")

        self.line("")

    # -----
    # _flash_habs
    # -----
    def _flash_habs(self) -> None:
        self.line("")

        if not self.confirm("Flash habs?"):
            return
        args = self._get_arg_list(["to"])
        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("flash habs", f"PLACEHOLDER {args} {self._optList} --no-interaction")

        self.line("")

    # -----
    # _flash_ex
    # -----
    def _flash_ex(self) -> None:
        self.line("")

        self.line("Flashing Execute")
        args = self._get_arg_list(["to", "rigidVersion", "motorType"])
        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("flash ex", f"PLACEHOLDER {args} {self._optList} --no-interaction")

        self.line("")

    # -----
    # _flash_re
    # -----
    def _flash_re(self) -> None:
        self.line("")

        self.line("Flashing Regulate")
        args = self._get_arg_list(["to", "rigidVersion", "led"])
        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("flash re", f"PLACEHOLDER {args} {self._optList} --no-interaction")

        self.line("")

    # -----
    # _flash_mn
    # -----
    def _flash_mn(self) -> None:
        self.line("")

        self.line("Flashing Manage")
        args = self._get_arg_list(["to", "rigidVersion", "device", "side"])
        # NOTE: There's a bug in cleo about how arguments are parsed when `call`
        # is used from an existing command. Basically, it skips the first word
        # given as an arg, so call('download tools', 'arg1 arg2') is interpreted
        # by cleo as trying to call the command `download tools arg2`, which is
        # wrong. The PLACEHOLDER should be removed when this is fixed
        # https://github.com/python-poetry/cleo/issues/130
        self.call("flash mn", f"PLACEHOLDER {args} {self._optList} --no-interaction")

        self.line("")

    # -----
    # _get_arg_list
    # -----
    def _get_arg_list(self, additionalArgs: List[str]) -> str:
        args = self._argList

        for arg in additionalArgs:
            if self.option(arg):
                args += f"{self.option(arg)} "
            else:
                msg = f"Please enter device's {arg} "
                msg += "(use `bootloader show --help` to see available options): "
                arg = self.ask(msg, None)
                if arg is None:
                    raise ValueError(f"Error: must enter a value for {arg}")
                args += f"{arg} "

        return args
