import bootloader.utilities.constants as bc


class UnsupportedOSError(Exception):
    """
    Raised when running on an unsupported operating system.
    """

    # -----
    # constructor
    # -----
    def __init__(self, currentOS) -> None:
        self._currentOS = currentOS

    # -----
    # __str__
    # -----
    def __str__(self) -> str:
        msg = "<error>Error: unsupported OS!"
        msg += f"\n\tDetected: <info>{self._currentOS}"
        msg += "\n\tSupported:"
        for operatingSystem in bc.supportedOS:
            msg += f"\n\t\t* <info>{operatingSystem}</info>"
        return msg
