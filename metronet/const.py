#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPLv3
"""
Support to interface with IESS Metronet.

For more details about this platform, please refer to the documentation at
https://community.home-assistant.io/t/echo-devices-alexa-as-media-player-testers-needed/58639
"""
from datetime import timedelta

__version__ = "0.1.0"
PROJECT_URL = "https://github.com/tulindo/metronet/"
ISSUE_URL = "{}issues".format(PROJECT_URL)

METRONET_BRIDGE = "metronet"
DOMAIN = "metronet"
DATA_METRONET = "metronet"

PLAY_SCAN_INTERVAL = 20
SCAN_INTERVAL = timedelta(seconds=60)
MIN_TIME_BETWEEN_SCANS = SCAN_INTERVAL
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=1)

METRONET_COMPONENTS = ["binary_sensor"]

CONF_SENSORS = "sensors"
CONF_DEBUG = "debug"
CONF_INCLUDE_DEVICES = "include_devices"
CONF_EXCLUDE_DEVICES = "exclude_devices"
SERVICE_UPDATE_LAST_CALLED = "update_last_called"
ATTR_MESSAGE = "message"
ATTR_EMAIL = "email"

STARTUP = """
-------------------------------------------------------------------
{}
Version: {}
This is a custom component
If you have any issues with this you need to open an issue here:
{}
-------------------------------------------------------------------
""".format(
    DOMAIN, __version__, ISSUE_URL
)
