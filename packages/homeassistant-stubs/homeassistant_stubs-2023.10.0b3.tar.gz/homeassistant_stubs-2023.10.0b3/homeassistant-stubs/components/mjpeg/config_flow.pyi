import voluptuous as vol
from .const import CONF_MJPEG_URL as CONF_MJPEG_URL, CONF_STILL_IMAGE_URL as CONF_STILL_IMAGE_URL, DOMAIN as DOMAIN, LOGGER as LOGGER
from _typeshed import Incomplete
from homeassistant.config_entries import ConfigEntry as ConfigEntry, ConfigFlow as ConfigFlow, OptionsFlow as OptionsFlow
from homeassistant.const import CONF_AUTHENTICATION as CONF_AUTHENTICATION, CONF_NAME as CONF_NAME, CONF_PASSWORD as CONF_PASSWORD, CONF_USERNAME as CONF_USERNAME, CONF_VERIFY_SSL as CONF_VERIFY_SSL, HTTP_BASIC_AUTHENTICATION as HTTP_BASIC_AUTHENTICATION, HTTP_DIGEST_AUTHENTICATION as HTTP_DIGEST_AUTHENTICATION
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from types import MappingProxyType
from typing import Any

def async_get_schema(defaults: dict[str, Any] | MappingProxyType[str, Any], show_name: bool = ...) -> vol.Schema: ...
def validate_url(url: str, username: str | None, password: str, verify_ssl: bool, authentication: str = ...) -> str: ...
async def async_validate_input(hass: HomeAssistant, user_input: dict[str, Any]) -> tuple[dict[str, str], str]: ...

class MJPEGFlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION: int
    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> MJPEGOptionsFlowHandler: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...

class MJPEGOptionsFlowHandler(OptionsFlow):
    config_entry: Incomplete
    def __init__(self, config_entry: ConfigEntry) -> None: ...
    async def async_step_init(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...

class InvalidAuth(HomeAssistantError): ...
