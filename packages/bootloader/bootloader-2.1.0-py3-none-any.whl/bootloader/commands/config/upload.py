import botocore.exceptions as bce
import boto3
from cleo.commands.command import Command as BaseCommand
from cleo.helpers import argument

import bootloader.utilities.constants as bc
from bootloader.utilities.help import config_upload_help


# ============================================
#            ConfigUploadCommand
# ============================================
class ConfigUploadCommand(BaseCommand):
    name = "config upload"
    description = "Uploads a configuration archive to S3."
    help = config_upload_help()
    hidden = False

    arguments = [argument("archiveName", "Name of the zip archive to upload.")]

    # -----
    # handle
    # -----
    def handle(self) -> int:
        self.line("")
        self.write("Uploading...")

        try:
            client = boto3.Session(profile_name=bc.dephyAwsProfile).client("s3")
        except bce.ProfileNotFound as err:
            msg = "Error: could not find valid 'dephy' profile in '~/.aws/credentials'."
            msg += " Could not upload configuration."
            raise RuntimeError(msg) from err

        archive = self.argument("archiveName")

        try:
            client.upload_file(archive, bc.dephyConfigsBucket, archive)
        except (bce.PartialCredentialsError, bce.NoCredentialsError) as err:
            msg = "Error: invalid credentials. Please check your access keys stored "
            msg += "in '~/.aws/credentials'."
            raise RuntimeError(msg) from err
        except bce.ClientError as err:
            msg = "Error: could not connect to S3. Upload failed."
            raise RuntimeError(msg) from err

        self.overwrite(f"Uploading... {self.application._SUCCESS}")

        return 0
