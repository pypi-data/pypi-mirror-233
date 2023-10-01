from .const import DOMAIN as DOMAIN
from .coordinator import SensiboDataUpdateCoordinator as SensiboDataUpdateCoordinator
from .entity import SensiboDeviceBaseEntity as SensiboDeviceBaseEntity, async_handle_api_call as async_handle_api_call
from _typeshed import Incomplete
from homeassistant.components.climate import ATTR_FAN_MODE as ATTR_FAN_MODE, ATTR_SWING_MODE as ATTR_SWING_MODE, ClimateEntity as ClimateEntity, ClimateEntityFeature as ClimateEntityFeature, HVACMode as HVACMode
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import ATTR_MODE as ATTR_MODE, ATTR_STATE as ATTR_STATE, ATTR_TEMPERATURE as ATTR_TEMPERATURE, PRECISION_TENTHS as PRECISION_TENTHS, UnitOfTemperature as UnitOfTemperature
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers import entity_platform as entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.util.unit_conversion import TemperatureConverter as TemperatureConverter
from typing import Any

SERVICE_ASSUME_STATE: str
SERVICE_ENABLE_TIMER: str
ATTR_MINUTES: str
SERVICE_ENABLE_PURE_BOOST: str
SERVICE_DISABLE_PURE_BOOST: str
SERVICE_FULL_STATE: str
SERVICE_ENABLE_CLIMATE_REACT: str
ATTR_HIGH_TEMPERATURE_THRESHOLD: str
ATTR_HIGH_TEMPERATURE_STATE: str
ATTR_LOW_TEMPERATURE_THRESHOLD: str
ATTR_LOW_TEMPERATURE_STATE: str
ATTR_SMART_TYPE: str
ATTR_AC_INTEGRATION: str
ATTR_GEO_INTEGRATION: str
ATTR_INDOOR_INTEGRATION: str
ATTR_OUTDOOR_INTEGRATION: str
ATTR_SENSITIVITY: str
ATTR_TARGET_TEMPERATURE: str
ATTR_HORIZONTAL_SWING_MODE: str
ATTR_LIGHT: str
BOOST_INCLUSIVE: str
AVAILABLE_FAN_MODES: Incomplete
AVAILABLE_SWING_MODES: Incomplete
PARALLEL_UPDATES: int
FIELD_TO_FLAG: Incomplete
SENSIBO_TO_HA: Incomplete
HA_TO_SENSIBO: Incomplete
AC_STATE_TO_DATA: Incomplete

def _find_valid_target_temp(target: int, valid_targets: list[int]) -> int: ...
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class SensiboClimate(SensiboDeviceBaseEntity, ClimateEntity):
    _attr_name: Incomplete
    _attr_precision = PRECISION_TENTHS
    _attr_translation_key: str
    _attr_unique_id: Incomplete
    _attr_temperature_unit: Incomplete
    _attr_supported_features: Incomplete
    def __init__(self, coordinator: SensiboDataUpdateCoordinator, device_id: str) -> None: ...
    def get_features(self) -> ClimateEntityFeature: ...
    @property
    def current_humidity(self) -> int | None: ...
    @property
    def hvac_mode(self) -> HVACMode: ...
    @property
    def hvac_modes(self) -> list[HVACMode]: ...
    @property
    def current_temperature(self) -> float | None: ...
    @property
    def temperature_unit(self) -> str: ...
    @property
    def target_temperature(self) -> float | None: ...
    @property
    def target_temperature_step(self) -> float | None: ...
    @property
    def fan_mode(self) -> str | None: ...
    @property
    def fan_modes(self) -> list[str] | None: ...
    @property
    def swing_mode(self) -> str | None: ...
    @property
    def swing_modes(self) -> list[str] | None: ...
    @property
    def min_temp(self) -> float: ...
    @property
    def max_temp(self) -> float: ...
    @property
    def available(self) -> bool: ...
    async def async_set_temperature(self, **kwargs: Any) -> None: ...
    async def async_set_fan_mode(self, fan_mode: str) -> None: ...
    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None: ...
    async def async_set_swing_mode(self, swing_mode: str) -> None: ...
    async def async_turn_on(self) -> None: ...
    async def async_turn_off(self) -> None: ...
    async def async_assume_state(self, state: str) -> None: ...
    async def async_full_ac_state(self, mode: str, target_temperature: int | None = ..., fan_mode: str | None = ..., swing_mode: str | None = ..., horizontal_swing_mode: str | None = ..., light: str | None = ...) -> None: ...
    async def async_enable_timer(self, minutes: int) -> None: ...
    async def async_enable_pure_boost(self, ac_integration: bool | None = ..., geo_integration: bool | None = ..., indoor_integration: bool | None = ..., outdoor_integration: bool | None = ..., sensitivity: str | None = ...) -> None: ...
    async def async_enable_climate_react(self, high_temperature_threshold: float, high_temperature_state: dict[str, Any], low_temperature_threshold: float, low_temperature_state: dict[str, Any], smart_type: str) -> None: ...
    async def async_send_api_call(self, key: str, value: Any, name: str, assumed_state: bool = ..., transformation: dict | None = ...) -> bool: ...
    async def api_call_custom_service_timer(self, key: str, value: Any, data: dict) -> bool: ...
    async def api_call_custom_service_pure_boost(self, key: str, value: Any, data: dict) -> bool: ...
    async def api_call_custom_service_climate_react(self, key: str, value: Any, data: dict) -> bool: ...
    async def api_call_custom_service_full_ac_state(self, key: str, value: Any, data: dict) -> bool: ...
