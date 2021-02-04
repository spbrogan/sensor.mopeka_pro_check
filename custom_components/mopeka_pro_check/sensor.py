"""Mopeka Propane Tank Level Sensor integration

Copyright (c) 2021 Sean Brogan
Copyright (c) 2020 Home-Is-Where-You-Hang-Your-Hack

SPDX-License-Identifier: MIT

"""
from datetime import timedelta
import logging
import voluptuous as vol
from typing import List

from mopeka_pro_check.service import MopekaService, GetServiceInstance
from mopeka_pro_check.sensor import MopekaSensor

from homeassistant.components.sensor import PLATFORM_SCHEMA  # type: ignore
import homeassistant.helpers.config_validation as cv  # type: ignore
from homeassistant.helpers.entity import Entity  # type: ignore
from homeassistant.helpers.event import track_point_in_utc_time  # type: ignore
import homeassistant.util.dt as dt_util  # type: ignore

from homeassistant.const import (  # type: ignore
    ATTR_BATTERY_LEVEL,
    CONF_MAC,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    PERCENTAGE,
)

from .const import (
    CONF_SUPPORTED_STD_TANK_NAMES,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_HCI_DEVICE,
    DEFAULT_STD_TANK,
    CONF_HCI_DEVICE,
    CONF_MOPEKA_DEVICES,
    CONF_TANK_TYPE,
    CONF_TANK_MAX_HEIGHT,
    CONF_SUPPORTED_STD_TANKS_MAP,
    CONF_TANK_TYPE_CUSTOM,
    CONF_TANK_TYPE_STD,
    CONF_TANK_FIELD,
    DOMAIN,
)

###############################################################################

_LOGGER = logging.getLogger(__name__)

DEVICES_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MAC): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_TANK_TYPE, default=CONF_TANK_TYPE_STD): vol.In((CONF_TANK_TYPE_STD, CONF_TANK_TYPE_CUSTOM)),
        vol.Optional(CONF_TANK_FIELD, default=DEFAULT_STD_TANK): vol.In(CONF_SUPPORTED_STD_TANK_NAMES),
        vol.Optional(CONF_TANK_MAX_HEIGHT): cv.positive_float
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): cv.positive_int,
        vol.Optional(CONF_MOPEKA_DEVICES): vol.All([DEVICES_SCHEMA]),
        vol.Optional(CONF_HCI_DEVICE, default=DEFAULT_HCI_DEVICE): cv.string,
    }
)

###############################################################################


#
# Configure for Home Assistant
#
def setup_platform(hass, config, add_entities, discovery_info=None) -> None:
    """Set up the sensor platform."""
    _LOGGER.debug("Starting Mopeka Tank Level Sensor")

    service: MopekaService = GetServiceInstance()

    def init_configured_devices() -> None:
        """Initialize configured mopeka devices."""
        for conf_dev in config[CONF_MOPEKA_DEVICES]:
            # Initialize sensor object
            mac = conf_dev[CONF_MAC]
            device = MopekaSensor(mac)
            device.name = conf_dev.get(CONF_NAME, mac)

            # Initialize HA sensors
            tank_sensor = TankLevelSensor(device._mac, device.name)
            device.ha_sensor = tank_sensor

            # find tank type
            tt = conf_dev.get(CONF_TANK_TYPE)
            if tt == CONF_TANK_TYPE_CUSTOM:
                # if max height missing uses 20 lbs vertical tank
                device.height = float(
                    conf_dev.get(
                        CONF_TANK_MAX_HEIGHT,
                        CONF_SUPPORTED_STD_TANKS_MAP[DEFAULT_STD_TANK].get(CONF_TANK_MAX_HEIGHT),
                    )
                )
                getattr(tank_sensor, "_device_state_attributes")[CONF_TANK_FIELD] = "n/a"
            else:
                std_type = conf_dev.get(CONF_TANK_FIELD)
                device.height = CONF_SUPPORTED_STD_TANKS_MAP[std_type].get(CONF_TANK_MAX_HEIGHT)
                getattr(tank_sensor, "_device_state_attributes")[CONF_TANK_FIELD] = std_type

            getattr(tank_sensor, "_device_state_attributes")[CONF_TANK_TYPE] = tt
            getattr(tank_sensor, "_device_state_attributes")["tank_height"] = device.height

            service.AddSensorToMonitor(device)
            add_entities((tank_sensor,))

    def update_ble_devices(config) -> None:
        """Discover Bluetooth LE devices."""
        # _LOGGER.debug("Discovering Bluetooth LE devices")

        ATTR = "_device_state_attributes"

        for device in service.SensorMonitoredList.values():
            sensor = device.ha_sensor
            ma = device.GetReading()
            if ma != None:
                sensor._tank_level = round(((ma.TankLevelInMM * 100.0) / device.height), 1)
                getattr(sensor, ATTR)["rssi"] = ma.rssi
                getattr(sensor, ATTR)["confidence_score"] = ma.ReadingQualityStars
                getattr(sensor, ATTR)["temp_c"] = ma.TemperatureInCelsius
                getattr(sensor, ATTR)["temp_f"] = ma.TemperatureInFahrenheit
                getattr(sensor, ATTR)[ATTR_BATTERY_LEVEL] = ma.BatteryPercent
                getattr(sensor, ATTR)["tank_level_mm"] = ma.TankLevelInMM
                sensor.async_schedule_update_ha_state()

    def update_ble_loop(now) -> None:
        """Lookup Bluetooth LE devices and update status."""
        _LOGGER.debug("update_ble_loop called")

        try:
            # Time to make the dounuts
            update_ble_devices(config)
        except RuntimeError as error:
            _LOGGER.error("Error during Bluetooth LE scan: %s", error)

        time_offset = dt_util.utcnow() + timedelta(seconds=config[CONF_SCAN_INTERVAL])
        # update_ble_loop() will be called again after time_offset
        track_point_in_utc_time(hass, update_ble_loop, time_offset)

    ###########################################################################

    HciIndex = int(config[CONF_HCI_DEVICE][-1])
    service.SetHostControllerIndex(HciIndex)

    hass.bus.listen("homeassistant_stop", service.Stop)

    # Initialize configured Mopeka devices
    init_configured_devices()
    service.Start()
    # Begin sensor update loop
    update_ble_loop(dt_util.utcnow())


###############################################################################

#
# HomeAssistant Tank Level Sensor
#
class TankLevelSensor(Entity):
    """Representation of a sensor."""

    def __init__(self, mac: str, name: str):
        """Initialize the sensor."""
        self._tank_level = None
        self._unique_id = "mopeka_" + mac.replace(":", "")
        self._name = name
        self._device_state_attributes = {}

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._tank_level

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def device_class(self):
        """There is no Defined Device Class for this tank level"""
        return None

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._device_state_attributes

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """ is the sensor available """
        return (self._tank_level is not None)

    @property
    def icon(self):
        return "mdi:propane-tank"

