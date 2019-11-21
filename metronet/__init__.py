#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPLv3
"""
Support to interface with IESS Metronet.

For more details about this platform, please refer to the documentation at
https://community.home-assistant.io/t/echo-devices-alexa-as-media-player-testers-needed/58639
"""
import logging
from typing import Optional, Text

import voluptuous as vol

from metronetpy import MetronetBridge
from homeassistant import util
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_ID,
    CONF_TYPE,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    CONF_URL,
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.event import async_call_later
from homeassistant.components.binary_sensor import DEVICE_CLASSES

from .const import (
    ATTR_EMAIL,
    CONF_SENSORS,
    CONF_DEBUG,
    METRONET_BRIDGE,
    CONF_EXCLUDE_DEVICES,
    CONF_INCLUDE_DEVICES,
    DOMAIN,
    MIN_TIME_BETWEEN_FORCED_SCANS,
    MIN_TIME_BETWEEN_SCANS,
    SCAN_INTERVAL,
    SERVICE_UPDATE_LAST_CALLED,
    STARTUP,
    __version__,
)

# from .config_flow import configured_instances

_LOGGER = logging.getLogger(__name__)

ATTR_DISCOVER_DEVICES = "metronet_sensor"

SENSORS_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ID): cv.positive_int,
        vol.Optional(CONF_TYPE): vol.In(DEVICE_CLASSES),
        vol.Optional(CONF_NAME): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_SENSORS): vol.All(
                    cv.ensure_list, [SENSORS_CONFIG_SCHEMA]
                ),
            }
        ),
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Set up the Metronet platform."""

    conf = config[DOMAIN]
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    _LOGGER.debug("Setting up Metronet Bridge")

    bridge = hass.data[METRONET_BRIDGE] = MetronetBridge(username, password)

    is_connected = bridge.connect()

    if is_connected:
        _LOGGER.info(f"Metroned connected {is_connected}")
        sensors = []
        for item in conf.get(CONF_SENSORS):
            sensor = {
                "id": item.get("id"),
                "type": item.get("type"),
                "name": item.get("name"),
            }
            sensors.append(sensor)

        bridge.load_config(sensors)

        sensors = bridge.get_sensors()

        # listen to home assistant stop event in order to stop the main loop
        def handle_stop_event(event):
            """Handle Home Assistant stop event."""
            bridge.stop()

        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, handle_stop_event)

        bridge.main_loop()

        # Get the sensors from the device and add those
        load_platform(
            hass, "binary_sensor", DOMAIN, {ATTR_DISCOVER_DEVICES: sensors}, config
        )

    return is_connected
