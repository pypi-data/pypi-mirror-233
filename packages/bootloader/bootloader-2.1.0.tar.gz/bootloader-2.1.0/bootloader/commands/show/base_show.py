from botocore.exceptions import ProfileNotFound
from cleo.commands.command import Command as BaseCommand
from cloudpathlib import CloudPath
from cloudpathlib import S3Client

import bootloader.utilities.constants as bc


# ============================================
#               BaseShowCommand
# ============================================
class BaseShowCommand(BaseCommand):
    # -----
    # _get_cloud_path
    # -----
    def _get_cloud_path(self, bucketName: str) -> CloudPath:
        try:
            client = S3Client(profile_name=bc.dephyAwsProfile)
        except ProfileNotFound as err:
            msg = "Error: could not find dephy profile in '~/.aws/credentials'. "
            msg += "Could not list desired information."
            raise RuntimeError(msg) from err

        # We use cloudpathlib here instead of flexsea's get_s3_objects
        # because it's a.) better, b.) separate from flexsea, and c.)
        # because get_s3_objects doesn't work when the objects you're
        # looking for are at the top level of the bucket and not in a
        # sub-folder. In general, I would like to switch to
        # cloudpathlib for all of the S3 operations in both flexsea and
        # the bootloader in the future
        return client.CloudPath(f"s3://{bucketName}/")

    # -----
    # handle
    # -----
    def handle(self) -> None:
        pass
