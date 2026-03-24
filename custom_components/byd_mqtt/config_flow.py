"""Config flow for BYD MQTT integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN, DEFAULT_TOPIC, CONF_TOPIC


class BYDMQTTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BYD MQTT."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # 可选：验证主题格式
            return self.async_create_entry(title="BYD MQTT", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_TOPIC, default=DEFAULT_TOPIC): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow."""
        return BYDMQTTOptionsFlow(config_entry)


class BYDMQTTOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_TOPIC,
                    default=self.config_entry.options.get(CONF_TOPIC, DEFAULT_TOPIC),
                ): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)