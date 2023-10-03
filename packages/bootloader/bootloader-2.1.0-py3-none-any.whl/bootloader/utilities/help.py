# ============================================
#                  mn_help
# ============================================
def mn_help() -> str:
    return "Flashes new firmware onto Manage."


# ============================================
#                  ex_help
# ============================================
def ex_help() -> str:
    return "Flashes new firmware onto Execute."


# ============================================
#                  re_help
# ============================================
def re_help() -> str:
    return "Flashes new firmware onto Regulate."


# ============================================
#                  habs_help
# ============================================
def habs_help() -> str:
    return "Flashes new firmware onto Habsolute."


# ============================================
#                  bt121_help
# ============================================
def bt121_help() -> str:
    return "Flashes new firmware onto Bt121."


# ============================================
#                  xbee_help
# ============================================
def xbee_help() -> str:
    return "Flashes new firmware onto Bt121."


# ============================================
#                  all_help
# ============================================
def all_help() -> str:
    return "Flashes new firmware onto xbee, bt121, habs, ex, re, and mn."


# ============================================
#                  tools_help
# ============================================
def tools_help() -> str:
    return "Downloads tools for bootloading."


# ============================================
#             config_create_help
# ============================================
def config_create_help() -> str:
    return "Creates a collection of files that can be flashed via `flash config`"


# ============================================
#             show_configs_help
# ============================================
def show_configs_help() -> str:
    return "Displays the available pre-made configurations for flashing."


# ============================================
#             flash_config_help
# ============================================
def flash_config_help() -> str:
    return "Flashes the files stored in the given config."


# ============================================
#            config_download_help
# ============================================
def config_download_help() -> str:
    return "Downloads the given configuration from S3."


# ============================================
#            config_upload_help
# ============================================
def config_upload_help() -> str:
    return "Uploads the given configuration to S3."


# ============================================
#            show_devices_help
# ============================================
def show_devices_help() -> str:
    return "Lists all devices for which there is firmware."


# ============================================
#            show_rigids_help
# ============================================
def show_rigids_help() -> str:
    return "Lists all rigid versions for which there is firmware."


# ============================================
#            show_versions_help
# ============================================
def show_versions_help() -> str:
    return "Lists all available firmware versions."
