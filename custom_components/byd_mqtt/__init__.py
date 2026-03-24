"""Init for BYD MQTT integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    DOMAIN,
    DEVICE_ID,
    DEVICE_NAME,
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    CONF_TOPIC,
    SERVICE_RESET_CACHE,
    DEFAULT_TOPIC,
)
from .data_handler import BYDDataHandler

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BYD MQTT from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    topic = entry.data.get(CONF_TOPIC, DEFAULT_TOPIC)

    # 检查 MQTT 集成是否已加载
    if "mqtt" not in hass.config.components:
        _LOGGER.error("MQTT integration is not loaded")
        return False

    # 创建设备注册
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, DEVICE_ID)},
        name=DEVICE_NAME,
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
    )

    # 初始化数据处理器
    handler = BYDDataHandler(hass, topic)
    await handler.async_subscribe()

    hass.data[DOMAIN][entry.entry_id] = {
        "handler": handler,
        "device_info": DeviceInfo(
            identifiers={(DOMAIN, DEVICE_ID)},
            name=DEVICE_NAME,
            manufacturer=DEVICE_MANUFACTURER,
            model=DEVICE_MODEL,
        ),
    }

    # 注册服务
    async def async_reset_cache(call: ServiceCall) -> None:
        """重置缓存服务."""
        handler.reset_cache()
        async_dispatcher_send(hass, f"{DOMAIN}_reset_cache")

    hass.services.async_register(DOMAIN, SERVICE_RESET_CACHE, async_reset_cache)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        handler = hass.data[DOMAIN][entry.entry_id]["handler"]
        await handler.async_unsubscribe()
        hass.data[DOMAIN].pop(entry.entry_id)

    # 移除服务
    hass.services.async_remove(DOMAIN, SERVICE_RESET_CACHE)

    return unload_ok