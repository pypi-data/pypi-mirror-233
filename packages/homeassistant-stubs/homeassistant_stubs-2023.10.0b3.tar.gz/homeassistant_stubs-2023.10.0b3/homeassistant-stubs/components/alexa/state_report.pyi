import aiohttp
from .config import AbstractConfig as AbstractConfig
from .const import API_CHANGE as API_CHANGE, API_CONTEXT as API_CONTEXT, API_DIRECTIVE as API_DIRECTIVE, API_ENDPOINT as API_ENDPOINT, API_EVENT as API_EVENT, API_HEADER as API_HEADER, API_PAYLOAD as API_PAYLOAD, API_SCOPE as API_SCOPE, Cause as Cause, DATE_FORMAT as DATE_FORMAT, DOMAIN as DOMAIN
from .entities import AlexaEntity as AlexaEntity, ENTITY_ADAPTERS as ENTITY_ADAPTERS, generate_alexa_id as generate_alexa_id
from .errors import AlexaInvalidEndpointError as AlexaInvalidEndpointError, NoTokenAvailable as NoTokenAvailable, RequireRelink as RequireRelink
from _typeshed import Incomplete
from homeassistant.components import event as event
from homeassistant.const import MATCH_ALL as MATCH_ALL, STATE_ON as STATE_ON
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, HomeAssistant as HomeAssistant, State as State, callback as callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from homeassistant.helpers.event import async_track_state_change as async_track_state_change
from homeassistant.helpers.significant_change import create_checker as create_checker
from homeassistant.util.json import JsonObjectType as JsonObjectType, json_loads_object as json_loads_object
from typing import Any

_LOGGER: Incomplete
DEFAULT_TIMEOUT: int

class AlexaDirective:
    entity: State
    entity_id: str | None
    endpoint: AlexaEntity
    instance: str | None
    _directive: Incomplete
    namespace: Incomplete
    name: Incomplete
    payload: Incomplete
    has_endpoint: Incomplete
    def __init__(self, request: dict[str, Any]) -> None: ...
    def load_entity(self, hass: HomeAssistant, config: AbstractConfig) -> None: ...
    def response(self, name: str = ..., namespace: str = ..., payload: dict[str, Any] | None = ...) -> AlexaResponse: ...
    def error(self, namespace: str = ..., error_type: str = ..., error_message: str = ..., payload: dict[str, Any] | None = ...) -> AlexaResponse: ...

class AlexaResponse:
    _response: Incomplete
    def __init__(self, name: str, namespace: str, payload: dict[str, Any] | None = ...) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def namespace(self) -> str: ...
    def set_correlation_token(self, token: str) -> None: ...
    def set_endpoint_full(self, bearer_token: str | None, endpoint_id: str | None) -> None: ...
    def set_endpoint(self, endpoint: dict[str, Any]) -> None: ...
    def _properties(self) -> list[dict[str, Any]]: ...
    def add_context_property(self, prop: dict[str, Any]) -> None: ...
    def merge_context_properties(self, endpoint: AlexaEntity) -> None: ...
    def serialize(self) -> dict[str, Any]: ...

async def async_enable_proactive_mode(hass: HomeAssistant, smart_home_config: AbstractConfig) -> CALLBACK_TYPE | None: ...
async def async_send_changereport_message(hass: HomeAssistant, config: AbstractConfig, alexa_entity: AlexaEntity, alexa_properties: list[dict[str, Any]], *, invalidate_access_token: bool = ...) -> None: ...
async def async_send_add_or_update_message(hass: HomeAssistant, config: AbstractConfig, entity_ids: list[str]) -> aiohttp.ClientResponse: ...
async def async_send_delete_message(hass: HomeAssistant, config: AbstractConfig, entity_ids: list[str]) -> aiohttp.ClientResponse: ...
async def async_send_doorbell_event_message(hass: HomeAssistant, config: AbstractConfig, alexa_entity: AlexaEntity) -> None: ...
