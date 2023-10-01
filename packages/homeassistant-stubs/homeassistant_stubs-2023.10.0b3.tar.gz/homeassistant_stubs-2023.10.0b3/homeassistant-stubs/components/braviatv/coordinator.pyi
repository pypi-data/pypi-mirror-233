from .const import CONF_CLIENT_ID as CONF_CLIENT_ID, CONF_NICKNAME as CONF_NICKNAME, CONF_USE_PSK as CONF_USE_PSK, DOMAIN as DOMAIN, LEGACY_CLIENT_ID as LEGACY_CLIENT_ID, NICKNAME_PREFIX as NICKNAME_PREFIX, SourceType as SourceType
from _typeshed import Incomplete
from collections.abc import Awaitable, Callable as Callable, Coroutine, Iterable
from homeassistant.components.media_player import MediaType as MediaType
from homeassistant.const import CONF_PIN as CONF_PIN
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed as ConfigEntryAuthFailed
from homeassistant.helpers.debounce import Debouncer as Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator as DataUpdateCoordinator, UpdateFailed as UpdateFailed
from pybravia import BraviaClient as BraviaClient
from types import MappingProxyType
from typing import Any, Concatenate, Final, TypeVar

_BraviaTVCoordinatorT = TypeVar('_BraviaTVCoordinatorT', bound='BraviaTVCoordinator')
_P: Incomplete
_LOGGER: Incomplete
SCAN_INTERVAL: Final[Incomplete]

def catch_braviatv_errors(func: Callable[Concatenate[_BraviaTVCoordinatorT, _P], Awaitable[None]]) -> Callable[Concatenate[_BraviaTVCoordinatorT, _P], Coroutine[Any, Any, None]]: ...

class BraviaTVCoordinator(DataUpdateCoordinator[None]):
    client: Incomplete
    pin: Incomplete
    use_psk: Incomplete
    client_id: Incomplete
    nickname: Incomplete
    source: Incomplete
    source_list: Incomplete
    source_map: Incomplete
    media_title: Incomplete
    media_channel: Incomplete
    media_content_id: Incomplete
    media_content_type: Incomplete
    media_uri: Incomplete
    media_duration: Incomplete
    volume_level: Incomplete
    volume_target: Incomplete
    volume_muted: bool
    is_on: bool
    connected: bool
    skipped_updates: int
    def __init__(self, hass: HomeAssistant, client: BraviaClient, config: MappingProxyType[str, Any]) -> None: ...
    def _sources_extend(self, sources: list[dict], source_type: SourceType, add_to_list: bool = ..., sort_by: str | None = ...) -> None: ...
    async def _async_update_data(self) -> None: ...
    async def async_update_volume(self) -> None: ...
    async def async_update_playing(self) -> None: ...
    async def async_update_sources(self) -> None: ...
    async def async_source_start(self, uri: str, source_type: SourceType | str) -> None: ...
    async def async_source_find(self, query: str, source_type: SourceType | str) -> None: ...
    async def async_turn_on(self) -> None: ...
    async def async_turn_off(self) -> None: ...
    async def async_set_volume_level(self, volume: float) -> None: ...
    async def async_volume_up(self) -> None: ...
    async def async_volume_down(self) -> None: ...
    async def async_volume_mute(self, mute: bool) -> None: ...
    async def async_media_play(self) -> None: ...
    async def async_media_pause(self) -> None: ...
    async def async_media_stop(self) -> None: ...
    async def async_media_next_track(self) -> None: ...
    async def async_media_previous_track(self) -> None: ...
    async def async_play_media(self, media_type: MediaType | str, media_id: str, **kwargs: Any) -> None: ...
    async def async_select_source(self, source: str) -> None: ...
    async def async_send_command(self, command: Iterable[str], repeats: int) -> None: ...
    async def async_reboot_device(self) -> None: ...
    async def async_terminate_apps(self) -> None: ...
