from . import storage as storage
from .device_registry import EVENT_DEVICE_REGISTRY_UPDATED as EVENT_DEVICE_REGISTRY_UPDATED
from .json import JSON_DUMP as JSON_DUMP, find_paths_unserializable_data as find_paths_unserializable_data
from .typing import UNDEFINED as UNDEFINED, UndefinedType as UndefinedType
from _typeshed import Incomplete
from collections import UserDict
from collections.abc import Callable as Callable, Iterable, Mapping, ValuesView
from enum import StrEnum
from homeassistant.backports.functools import cached_property as cached_property
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import ATTR_DEVICE_CLASS as ATTR_DEVICE_CLASS, ATTR_FRIENDLY_NAME as ATTR_FRIENDLY_NAME, ATTR_ICON as ATTR_ICON, ATTR_RESTORED as ATTR_RESTORED, ATTR_SUPPORTED_FEATURES as ATTR_SUPPORTED_FEATURES, ATTR_UNIT_OF_MEASUREMENT as ATTR_UNIT_OF_MEASUREMENT, EVENT_HOMEASSISTANT_START as EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP as EVENT_HOMEASSISTANT_STOP, EntityCategory as EntityCategory, MAX_LENGTH_STATE_DOMAIN as MAX_LENGTH_STATE_DOMAIN, MAX_LENGTH_STATE_ENTITY_ID as MAX_LENGTH_STATE_ENTITY_ID, Platform as Platform, STATE_UNAVAILABLE as STATE_UNAVAILABLE, STATE_UNKNOWN as STATE_UNKNOWN
from homeassistant.core import Event as Event, HomeAssistant as HomeAssistant, callback as callback, split_entity_id as split_entity_id, valid_entity_id as valid_entity_id
from homeassistant.exceptions import MaxLengthExceeded as MaxLengthExceeded
from homeassistant.util import slugify as slugify
from homeassistant.util.json import format_unserializable_data as format_unserializable_data
from homeassistant.util.read_only_dict import ReadOnlyDict as ReadOnlyDict
from typing import Any, Literal, NotRequired, TypeVar, TypedDict

T = TypeVar('T')
DATA_REGISTRY: str
EVENT_ENTITY_REGISTRY_UPDATED: str
SAVE_DELAY: int
_LOGGER: Incomplete
STORAGE_VERSION_MAJOR: int
STORAGE_VERSION_MINOR: int
STORAGE_KEY: str
CLEANUP_INTERVAL: Incomplete
ORPHANED_ENTITY_KEEP_SECONDS: Incomplete
ENTITY_CATEGORY_VALUE_TO_INDEX: dict[EntityCategory | None, int]
ENTITY_CATEGORY_INDEX_TO_VALUE: Incomplete
ENTITY_DESCRIBING_ATTRIBUTES: Incomplete

class RegistryEntryDisabler(StrEnum):
    CONFIG_ENTRY: str
    DEVICE: str
    HASS: str
    INTEGRATION: str
    USER: str

class RegistryEntryHider(StrEnum):
    INTEGRATION: str
    USER: str

class _EventEntityRegistryUpdatedData_CreateRemove(TypedDict):
    action: Literal['create', 'remove']
    entity_id: str

class _EventEntityRegistryUpdatedData_Update(TypedDict):
    action: Literal['update']
    entity_id: str
    changes: dict[str, Any]
    old_entity_id: NotRequired[str]

EventEntityRegistryUpdatedData: Incomplete
EntityOptionsType = Mapping[str, Mapping[str, Any]]
ReadOnlyEntityOptionsType = ReadOnlyDict[str, Mapping[str, Any]]
DISLAY_DICT_OPTIONAL: Incomplete

def _protect_entity_options(data: EntityOptionsType | None) -> ReadOnlyEntityOptionsType: ...

class RegistryEntry:
    entity_id: str
    unique_id: str
    platform: str
    aliases: set[str]
    area_id: str | None
    capabilities: Mapping[str, Any] | None
    config_entry_id: str | None
    device_class: str | None
    device_id: str | None
    domain: str
    disabled_by: RegistryEntryDisabler | None
    entity_category: EntityCategory | None
    hidden_by: RegistryEntryHider | None
    icon: str | None
    id: str
    has_entity_name: bool
    name: str | None
    options: ReadOnlyEntityOptionsType
    original_device_class: str | None
    original_icon: str | None
    original_name: str | None
    supported_features: int
    translation_key: str | None
    unit_of_measurement: str | None
    def _domain_default(self) -> str: ...
    @property
    def disabled(self) -> bool: ...
    @property
    def hidden(self) -> bool: ...
    @property
    def _as_display_dict(self) -> dict[str, Any] | None: ...
    def display_json_repr(self) -> str | None: ...
    @property
    def as_partial_dict(self) -> dict[str, Any]: ...
    def partial_json_repr(self) -> str | None: ...
    def write_unavailable_state(self, hass: HomeAssistant) -> None: ...
    def __init__(self, entity_id, unique_id, platform, aliases, area_id, capabilities, config_entry_id, device_class, device_id, domain, disabled_by, entity_category, hidden_by, icon, id, has_entity_name, name, options, original_device_class, original_icon, original_name, supported_features, translation_key, unit_of_measurement) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

class DeletedRegistryEntry:
    entity_id: str
    unique_id: str
    platform: str
    config_entry_id: str | None
    domain: str
    id: str
    orphaned_timestamp: float | None
    def _domain_default(self) -> str: ...
    def __init__(self, entity_id, unique_id, platform, config_entry_id, domain, id, orphaned_timestamp) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

class EntityRegistryStore(storage.Store[dict[str, list[dict[str, Any]]]]):
    async def _async_migrate_func(self, old_major_version: int, old_minor_version: int, old_data: dict[str, list[dict[str, Any]]]) -> dict: ...

class EntityRegistryItems(UserDict[str, RegistryEntry]):
    _entry_ids: Incomplete
    _index: Incomplete
    def __init__(self) -> None: ...
    def values(self) -> ValuesView[RegistryEntry]: ...
    def __setitem__(self, key: str, entry: RegistryEntry) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def get_entity_id(self, key: tuple[str, str, str]) -> str | None: ...
    def get_entry(self, key: str) -> RegistryEntry | None: ...

class EntityRegistry:
    deleted_entities: dict[tuple[str, str, str], DeletedRegistryEntry]
    entities: EntityRegistryItems
    _entities_data: dict[str, RegistryEntry]
    hass: Incomplete
    _store: Incomplete
    def __init__(self, hass: HomeAssistant) -> None: ...
    def async_get_device_class_lookup(self, domain_device_classes: set[tuple[str, str | None]]) -> dict[str, dict[tuple[str, str | None], str]]: ...
    def async_is_registered(self, entity_id: str) -> bool: ...
    def async_get(self, entity_id_or_uuid: str) -> RegistryEntry | None: ...
    def async_get_entity_id(self, domain: str, platform: str, unique_id: str) -> str | None: ...
    def _entity_id_available(self, entity_id: str, known_object_ids: Iterable[str] | None) -> bool: ...
    def async_generate_entity_id(self, domain: str, suggested_object_id: str, known_object_ids: Iterable[str] | None = ...) -> str: ...
    def async_get_or_create(self, domain: str, platform: str, unique_id: str, *, known_object_ids: Iterable[str] | None = ..., suggested_object_id: str | None = ..., disabled_by: RegistryEntryDisabler | None = ..., hidden_by: RegistryEntryHider | None = ..., get_initial_options: Callable[[], EntityOptionsType | None] | None = ..., capabilities: Mapping[str, Any] | None | UndefinedType = ..., config_entry: ConfigEntry | None | UndefinedType = ..., device_id: str | None | UndefinedType = ..., entity_category: EntityCategory | UndefinedType | None = ..., has_entity_name: bool | UndefinedType = ..., original_device_class: str | None | UndefinedType = ..., original_icon: str | None | UndefinedType = ..., original_name: str | None | UndefinedType = ..., supported_features: int | None | UndefinedType = ..., translation_key: str | None | UndefinedType = ..., unit_of_measurement: str | None | UndefinedType = ...) -> RegistryEntry: ...
    def async_remove(self, entity_id: str) -> None: ...
    def async_device_modified(self, event: Event) -> None: ...
    def _async_update_entity(self, entity_id: str, *, aliases: set[str] | UndefinedType = ..., area_id: str | None | UndefinedType = ..., capabilities: Mapping[str, Any] | None | UndefinedType = ..., config_entry_id: str | None | UndefinedType = ..., device_class: str | None | UndefinedType = ..., device_id: str | None | UndefinedType = ..., disabled_by: RegistryEntryDisabler | None | UndefinedType = ..., entity_category: EntityCategory | None | UndefinedType = ..., hidden_by: RegistryEntryHider | None | UndefinedType = ..., icon: str | None | UndefinedType = ..., has_entity_name: bool | UndefinedType = ..., name: str | None | UndefinedType = ..., new_entity_id: str | UndefinedType = ..., new_unique_id: str | UndefinedType = ..., options: EntityOptionsType | UndefinedType = ..., original_device_class: str | None | UndefinedType = ..., original_icon: str | None | UndefinedType = ..., original_name: str | None | UndefinedType = ..., platform: str | None | UndefinedType = ..., supported_features: int | UndefinedType = ..., translation_key: str | None | UndefinedType = ..., unit_of_measurement: str | None | UndefinedType = ...) -> RegistryEntry: ...
    def async_update_entity(self, entity_id: str, *, aliases: set[str] | UndefinedType = ..., area_id: str | None | UndefinedType = ..., capabilities: Mapping[str, Any] | None | UndefinedType = ..., config_entry_id: str | None | UndefinedType = ..., device_class: str | None | UndefinedType = ..., device_id: str | None | UndefinedType = ..., disabled_by: RegistryEntryDisabler | None | UndefinedType = ..., entity_category: EntityCategory | None | UndefinedType = ..., hidden_by: RegistryEntryHider | None | UndefinedType = ..., icon: str | None | UndefinedType = ..., has_entity_name: bool | UndefinedType = ..., name: str | None | UndefinedType = ..., new_entity_id: str | UndefinedType = ..., new_unique_id: str | UndefinedType = ..., original_device_class: str | None | UndefinedType = ..., original_icon: str | None | UndefinedType = ..., original_name: str | None | UndefinedType = ..., supported_features: int | UndefinedType = ..., translation_key: str | None | UndefinedType = ..., unit_of_measurement: str | None | UndefinedType = ...) -> RegistryEntry: ...
    def async_update_entity_platform(self, entity_id: str, new_platform: str, *, new_config_entry_id: str | UndefinedType = ..., new_unique_id: str | UndefinedType = ..., new_device_id: str | None | UndefinedType = ...) -> RegistryEntry: ...
    def async_update_entity_options(self, entity_id: str, domain: str, options: Mapping[str, Any] | None) -> RegistryEntry: ...
    async def async_load(self) -> None: ...
    def async_schedule_save(self) -> None: ...
    def _data_to_save(self) -> dict[str, Any]: ...
    def async_clear_config_entry(self, config_entry_id: str) -> None: ...
    def async_purge_expired_orphaned_entities(self) -> None: ...
    def async_clear_area_id(self, area_id: str) -> None: ...

def async_get(hass: HomeAssistant) -> EntityRegistry: ...
async def async_load(hass: HomeAssistant) -> None: ...
def async_entries_for_device(registry: EntityRegistry, device_id: str, include_disabled_entities: bool = ...) -> list[RegistryEntry]: ...
def async_entries_for_area(registry: EntityRegistry, area_id: str) -> list[RegistryEntry]: ...
def async_entries_for_config_entry(registry: EntityRegistry, config_entry_id: str) -> list[RegistryEntry]: ...
def async_config_entry_disabled_by_changed(registry: EntityRegistry, config_entry: ConfigEntry) -> None: ...
def _async_setup_cleanup(hass: HomeAssistant, registry: EntityRegistry) -> None: ...
def _async_setup_entity_restore(hass: HomeAssistant, registry: EntityRegistry) -> None: ...
async def async_migrate_entries(hass: HomeAssistant, config_entry_id: str, entry_callback: Callable[[RegistryEntry], dict[str, Any] | None]) -> None: ...
def async_validate_entity_id(registry: EntityRegistry, entity_id_or_uuid: str) -> str: ...
def async_resolve_entity_id(registry: EntityRegistry, entity_id_or_uuid: str) -> str | None: ...
def async_validate_entity_ids(registry: EntityRegistry, entity_ids_or_uuids: list[str]) -> list[str]: ...
