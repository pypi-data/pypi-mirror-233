import os
from pathlib import Path
import subprocess as sub
from time import sleep
from typing import List

from flexsea.utilities.aws import s3_download
import flexsea.utilities.constants as fxc

import bootloader.utilities.constants as bc


# ============================================
#                setup_cache
# ============================================
def setup_cache() -> None:
    bc.firmwarePath.mkdir(parents=True, exist_ok=True)
    bc.toolsPath.mkdir(parents=True, exist_ok=True)
    bc.configsPath.mkdir(parents=True, exist_ok=True)


# ============================================
#             run_command
# ============================================
def run_command(cmd: List[str]) -> None:
    """
    Attempts to call the command `cmd`. If the call fails, we
    try again until the max attempts have been reached.
    """
    # This is done to prevent unboundlocalerror, which happens if
    # a calledprocesserror is raised if the process never successfully
    # completes
    proc = None

    for _ in range(5):
        try:
            proc = sub.run(
                cmd,
                capture_output=False,
                check=True,
                timeout=360,
                shell=True,
                env=os.environ,
            )
        except sub.CalledProcessError:
            sleep(1)
            continue
        except sub.TimeoutExpired as err:
            raise sub.TimeoutExpired(cmd, 360) from err
        if proc.returncode == 0:
            break
    if proc is None or proc.returncode != 0:
        raise RuntimeError(f"Error: command: `{cmd}` failed.")


# ============================================
#               get_fw_file
# ============================================
def get_fw_file(fName: str) -> Path:
    fwFile = fxc.dephyPath.joinpath(bc.firmwareDir, fName)

    if not fwFile.is_file():
        s3_download(str(fName), bc.dephyFirmwareBucket, str(fwFile), bc.dephyAwsProfile)

    return fwFile


# ============================================
#             psoc_flash_command
# ============================================
def psoc_flash_command(port: str, fwFile: str, opSys: str) -> List[str]:
    flashCmd = [
        f"{Path.joinpath(bc.toolsPath, opSys, 'psocbootloaderhost.exe')}",
        f"{port}",
        f"{fwFile}",
    ]

    return flashCmd
