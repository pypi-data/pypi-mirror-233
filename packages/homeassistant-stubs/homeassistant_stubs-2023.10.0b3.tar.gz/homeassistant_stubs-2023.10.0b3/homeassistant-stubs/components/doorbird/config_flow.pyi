import voluptuous as vol
from .const import CONF_EVENTS as CONF_EVENTS, DOMAIN as DOMAIN, DOORBIRD_OUI as DOORBIRD_OUI
from .util import get_mac_address_from_door_station_info as get_mac_address_from_door_station_info
from _typeshed import Incomplete
from doorbirdpy import DoorBird
from homeassistant import config_entries as config_entries, core as core, exceptions as exceptions
from homeassistant.components import zeroconf as zeroconf
from homeassistant.const import CONF_HOST as CONF_HOST, CONF_NAME as CONF_NAME, CONF_PASSWORD as CONF_PASSWORD, CONF_USERNAME as CONF_USERNAME
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from typing import Any

_LOGGER: Incomplete

def _schema_with_defaults(host: str | None = ..., name: str | None = ...) -> vol.Schema: ...
def _check_device(device: DoorBird) -> tuple[tuple[bool, int], dict[str, Any]]: ...
async def validate_input(hass: core.HomeAssistant, data: dict[str, Any]) -> dict[str, str]: ...
async def async_verify_supported_device(hass: HomeAssistant, host: str) -> bool: ...

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION: int
    discovery_schema: Incomplete
    def __init__(self) -> None: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_zeroconf(self, discovery_info: zeroconf.ZeroconfServiceInfo) -> FlowResult: ...
    async def _async_validate_or_error(self, user_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]: ...
    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlowHandler: ...

class OptionsFlowHandler(config_entries.OptionsFlow):
    config_entry: Incomplete
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None: ...
    async def async_step_init(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...

class CannotConnect(exceptions.HomeAssistantError): ...
class InvalidAuth(exceptions.HomeAssistantError): ...
