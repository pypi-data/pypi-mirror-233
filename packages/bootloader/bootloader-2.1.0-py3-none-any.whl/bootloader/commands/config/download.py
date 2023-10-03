from zipfile import ZipFile

import boto3
from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument
from flexsea.utilities.aws import s3_download
from flexsea.utilities.aws import s3_find_object

import bootloader.utilities.constants as bc
from bootloader.utilities.help import config_download_help


# ============================================
#           ConfigDownloadCommand
# ============================================
class ConfigDownloadCommand(BaseCommand):
    name = "config download"
    description = "Downloads the configuration archive with the given name from S3."
    help = config_download_help()

    arguments = [argument("archiveName", "Name of the archive to download.")]

    # -----
    # handle
    # -----
    def handle(self) -> int:
        archiveName = self.argument("archiveName") + ".zip"

        self.line("")
        self.write("Connecting to S3...")
        session = boto3.Session(profile_name=bc.dephyAwsProfile)
        client = session.client("s3")
        self.overwrite(f"Connecting to S3... {self.application._SUCCESS}")

        self.line("")
        self.write("Searching for archive...")
        archivePath = s3_find_object(archiveName, bc.dephyConfigsBucket, client)
        self.overwrite(f"Searching for archive... {self.application._SUCCESS}")

        self.line("")
        self.write("Downloading archive...")
        dest = str(bc.configsPath.joinpath(archiveName))
        s3_download(archivePath, bc.dephyConfigsBucket, dest, bc.dephyAwsProfile)
        self.overwrite(f"Downloading archive... {self.application._SUCCESS}")

        self.line("")
        self.write("Extracting archive...")
        extractionDest = bc.configsPath.joinpath(self.argument("archiveName"))
        extractionDest.mkdir(parents=True, exist_ok=True)
        with ZipFile(dest, "r") as archive:
            archive.extractall(path=extractionDest)
        self.overwrite(f"Extracting archive... {self.application._SUCCESS}")

        return 0
