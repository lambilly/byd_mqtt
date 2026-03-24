"""Binary sensor platform for BYD MQTT integration."""
import logging
from typing import Any, Dict

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, BINARY_SENSORS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""
    device_info = hass.data[DOMAIN][entry.entry_id]["device_info"]
    handler = hass.data[DOMAIN][entry.entry_id]["handler"]

    entities = []
    for sensor_id, name in BINARY_SENSORS:
        entities.append(
            BYDBinarySensor(
                device_info,
                sensor_id,
                name,
                handler,
            )
        )
    async_add_entities(entities)


class BYDBinarySensor(BinarySensorEntity):
    """Representation of a BYD binary sensor (windows)."""

    def __init__(
        self,
        device_info: DeviceInfo,
        sensor_id: str,
        name: str,
        handler,
    ) -> None:
        self._attr_device_info = device_info
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}"
        self._attr_name = name
        self._handler = handler
        self._sensor_id = sensor_id

    async def async_added_to_hass(self):
        """Register dispatcher."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"{DOMAIN}_new_data",
                self._handle_new_data,
            )
        )
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"{DOMAIN}_reset_cache",
                self._handle_reset,
            )
        )

    @callback
    def _handle_new_data(self, payload: Dict[str, Any]):
        """Handle new data."""
        cache = payload["cache"]
        if self._sensor_id == "byd_windows":
            # 窗口映射（与 Node-RED 完全一致）
            windows = {
                "左前窗": cache.get("window_lf"),
                "右前窗": cache.get("window_rf"),
                "左后窗": cache.get("window_lr"),
                "右后窗": cache.get("window_rr"),
                "天窗": cache.get("window_moon"),
            }
            # 过滤掉 None 值（尚未收到数据）
            valid = [v for v in windows.values() if v is not None]
            if valid:
                any_open = any(v != 0 for v in valid)
                self._attr_is_on = any_open
                self._attr_extra_state_attributes = {
                    k: ("打开" if v and v != 0 else "关闭")
                    for k, v in windows.items()
                }
            else:
                # 如果没有数据，保持原状态，不做改变（避免从 ON 变 OFF）
                pass

            self.async_write_ha_state()

    @callback
    def _handle_reset(self):
        """Handle cache reset."""
        self._attr_is_on = None
        self._attr_extra_state_attributes = {}
        self.async_write_ha_state()