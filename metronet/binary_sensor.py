"""Support for exposing Metronet elements as sensors."""
import datetime
import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import (
    DEVICE_CLASSES,
    PLATFORM_SCHEMA,
    BinarySensorDevice,
)
from . import ATTR_DISCOVER_DEVICES, METRONET_BRIDGE
from homeassistant.const import CONF_HOST, CONF_PORT
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)

CONF_EXCLUDE_SENSORS = "exclude_sensors"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_EXCLUDE_SENSORS, default=[]): vol.All(
            cv.ensure_list, [cv.positive_int]
        ),
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Metronet binary sensor platform."""

    if discovery_info is None or discovery_info[ATTR_DISCOVER_DEVICES] is None:
        return

    sensors = []

    for sensor in discovery_info[ATTR_DISCOVER_DEVICES]:
        _LOGGER.info("Loading Sensor found: %s", sensor["name"])
        # if sensor["id"] not in exclude:
        sensors.append(MetronetSensor(hass, sensor))

    async_add_entities(sensors, True)


class MetronetSensor(BinarySensorDevice):
    """Representation of a Metronet input as a binary sensor."""

    def __init__(self, hass, sensor):
        """Initialize the Metronet binary sensor."""
        self._hass = hass
        self._sensor = sensor
        self._id = sensor["id"]
        bridge = hass.data[METRONET_BRIDGE]
        bridge.register_callback(self._id, self.callback)

    def callback(self, id, is_active):
        self._sensor["active"] = is_active
        self.schedule_update_ha_state()

    @property
    def device_class(self):
        """Return the class of this sensor, from DEVICE_CLASSES."""
        return self._sensor["type"]

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return self._sensor["name"]

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        # True means "faulted" or "open" or "abnormal state
        return self._sensor["active"]

    def update(self):
        """Get updated stats from API."""

        # last_update = dt_util.utcnow() - self._client.last_sensor_update
        # _LOGGER.debug("Sensor: %s ", self._sensor)
        # if last_update > datetime.timedelta(seconds=1):
        #     self._client.sensors = self._client.list_sensors()
        #     self._client.last_sensor_update = dt_util.utcnow()
        #     _LOGGER.debug("Updated from sensor: %s", self._sensor["name"])

        # if hasattr(self._client, "sensors"):
        #     self._sensor = next(
        #         (x for x in self._client.sensors if x["id"] == self._id), None
        #     )
