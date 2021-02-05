"""Constants for the Mopeka Propane Tank Level Sensor BLE Home Assistant Component

Copyright (c) 2021 Sean Brogan
Copyright (c) 2020 Home-Is-Where-You-Hang-Your-Hack

SPDX-License-Identifier: MIT

"""

"""Fixed constants."""

DOMAIN = "mopeka_pro_check"

# Configuration options
CONF_HCI_DEVICE = "hci_device"
CONF_MOPEKA_DEVICES = "mopeka_devices"
CONF_TANK_TYPE = "tank_type"
CONF_TANK_MAX_HEIGHT = "max_height"
CONF_TANK_FIELD = "tank"

CONF_TANK_TYPE_CUSTOM = "custom"
CONF_TANK_TYPE_STD = "standard"
#
# HEIGHT in MM
#
CONF_SUPPORTED_STD_TANKS_MAP = {
    # Map these at about 67% of the tank height which seems like
    # 100% tank full
    "20lb_v": {CONF_TANK_MAX_HEIGHT: 302.84},   #452.12},  
    "30lb_v": {CONF_TANK_MAX_HEIGHT: 403.32},   #601.98},  
    "40lb_v": {CONF_TANK_MAX_HEIGHT: 498.62}    #744.22},
}

CONF_SUPPORTED_STD_TANK_NAMES = tuple(CONF_SUPPORTED_STD_TANKS_MAP.keys())

# use CONF_MAC, CONF_NAME, CONF_SCAN_INTERVAL


# Default values for configuration options
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_HCI_DEVICE = "hci0"
DEFAULT_STD_TANK = CONF_SUPPORTED_STD_TANK_NAMES[0]
