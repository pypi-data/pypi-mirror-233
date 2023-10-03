from flexsea.utilities.constants import dephyPath


# ============================================
#              Path Configuration
# ============================================

# toolsDir is the name of the directory (mirrored on S3), whereas
# toolsPath is the full path to that directory on the local file system
toolsDir = "bootloader_tools"
toolsPath = dephyPath.joinpath(toolsDir)

# firmwareDir is the name of the directory (mirrored on S3), whereas
# firmwarePath is the full path to that directory on the local file system
firmwareDir = "firmware"
firmwarePath = dephyPath.joinpath(firmwareDir)

# configsDir is the name of the directory (mirrored on S3), whereas
# configsPath is the full path to that directory on the local file system
configsDir = "configs"
configsPath = dephyPath.joinpath(configsDir)

# firstSetup is an empty file indicating first time setup has been run
# (installing mingw, dfuse folder, run st link for drivers)
firstSetup = dephyPath.joinpath(".first")


# ============================================
#              S3 Configuration
# ============================================

# Private bucket where the firmware is stored
dephyFirmwareBucket = "dephy-firmware-files"

# Credentials profile name
dephyAwsProfile = "dephy"

# Private bucket where firmware configurations are stored
dephyConfigsBucket = "dephy-configs"


# ============================================
#                Dependencies
# ============================================
bootloaderTools = {
    "windows_64bit": {
        "bt121": [
            "bt121_image_tools.zip",
            "stm32flash.exe",
        ],
        "ex": [
            "psocbootloaderhost.exe",
        ],
        "habs": [
            "stm32_flash_loader.zip",
        ],
        "mn": [
            "DfuSeCommand.exe",
        ],
        "re": [
            "psocbootloaderhost.exe",
        ],
        "xbee": [
            "XB24C.zip",
        ],
        "setup": [
            "dfuse_command.zip",
            "mingw.zip",
            "stlink_setup.exe",
            "DfuSe_Demo_V3.0.6_Setup.exe",
        ],
    },
    "windows_32bit": {
        "bt121": [
            "bt121_image_tools.zip",
            "stm32flash.exe",
        ],
        "ex": [
            "psocbootloaderhost.exe",
        ],
        "habs": [
            "stm32_flash_loader.zip",
        ],
        "mn": [
            "DfuSeCommand.exe",
        ],
        "re": [
            "psocbootloaderhost.exe",
        ],
        "xbee": [
            "XB24C.zip",
        ],
        "setup": [
            "dfuse_command.zip",
            "mingw.zip",
            "stlink_setup.exe",
            "DfuSe_Demo_V3.0.6_Setup.exe",
        ],
    },
}


# ============================================
#                 Constants
# ============================================
firmwareExtensions = {"habs": "hex", "ex": "cyacd", "re": "cyacd", "mn": "dfu"}
targets = ["habs", "ex", "re", "bt121", "xbee", "mn"]
supportedOS = [
    "windows_64bit",
    "windows_32bit",
]
supportedWindowsVersions = [
    "7",
    "8",
    "8.1",
    "10",
    "11",
]


# ============================================
#    Info for working with Configurations
# ============================================
configInfoFile = "config_info.yaml"


# ============================================
#                   Themes
# ============================================
themes = {
    "classic": {
        "info": {"foreground": "blue", "options": []},
        "warning": {"foreground": "yellow", "options": []},
        "error": {
            "foreground": "red",
            "options": [
                "bold",
            ],
        },
        "success": {
            "foreground": "green",
            "options": [
                "bold",
            ],
        },
    },
    "light": {
        "info": {"foreground": "light_blue", "options": []},
        "warning": {"foreground": "light_yellow", "options": []},
        "error": {
            "foreground": "light_red",
            "options": [
                "bold",
            ],
        },
        "success": {
            "foreground": "light_green",
            "options": [
                "bold",
            ],
        },
    },
    "dark": {
        "info": {
            "foreground": "blue",
            "options": [
                "dark",
            ],
        },
        "warning": {
            "foreground": "yellow",
            "options": [
                "dark",
            ],
        },
        "error": {
            "foreground": "red",
            "options": [
                "dark",
                "bold",
            ],
        },
        "success": {
            "foreground": "green",
            "options": [
                "dark",
                "bold",
            ],
        },
    },
    "default": {
        "info": {"foreground": "default", "options": []},
        "warning": {"foreground": "default", "options": []},
        "error": {"foreground": "default", "options": []},
        "success": {"foreground": "default", "options": []},
    },
}
