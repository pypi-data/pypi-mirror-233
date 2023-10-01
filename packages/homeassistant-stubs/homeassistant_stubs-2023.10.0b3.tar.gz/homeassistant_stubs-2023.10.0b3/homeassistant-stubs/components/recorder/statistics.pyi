from . import Recorder as Recorder
from .const import DOMAIN as DOMAIN, EVENT_RECORDER_5MIN_STATISTICS_GENERATED as EVENT_RECORDER_5MIN_STATISTICS_GENERATED, EVENT_RECORDER_HOURLY_STATISTICS_GENERATED as EVENT_RECORDER_HOURLY_STATISTICS_GENERATED, INTEGRATION_PLATFORM_COMPILE_STATISTICS as INTEGRATION_PLATFORM_COMPILE_STATISTICS, INTEGRATION_PLATFORM_LIST_STATISTIC_IDS as INTEGRATION_PLATFORM_LIST_STATISTIC_IDS, INTEGRATION_PLATFORM_VALIDATE_STATISTICS as INTEGRATION_PLATFORM_VALIDATE_STATISTICS, SupportedDialect as SupportedDialect
from .db_schema import STATISTICS_TABLES as STATISTICS_TABLES, Statistics as Statistics, StatisticsBase as StatisticsBase, StatisticsRuns as StatisticsRuns, StatisticsShortTerm as StatisticsShortTerm
from .models import StatisticData as StatisticData, StatisticDataTimestamp as StatisticDataTimestamp, StatisticMetaData as StatisticMetaData, StatisticResult as StatisticResult, datetime_to_timestamp_or_none as datetime_to_timestamp_or_none, process_timestamp as process_timestamp
from .util import execute as execute, execute_stmt_lambda_element as execute_stmt_lambda_element, get_instance as get_instance, retryable_database_job as retryable_database_job, session_scope as session_scope
from _typeshed import Incomplete
from collections.abc import Callable as Callable, Iterable, Sequence
from datetime import datetime, timedelta
from homeassistant.const import ATTR_UNIT_OF_MEASUREMENT as ATTR_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback, valid_entity_id as valid_entity_id
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.singleton import singleton as singleton
from homeassistant.helpers.typing import UNDEFINED as UNDEFINED, UndefinedType as UndefinedType
from homeassistant.util.unit_conversion import BaseUnitConverter as BaseUnitConverter, DataRateConverter as DataRateConverter, DistanceConverter as DistanceConverter, ElectricCurrentConverter as ElectricCurrentConverter, ElectricPotentialConverter as ElectricPotentialConverter, EnergyConverter as EnergyConverter, InformationConverter as InformationConverter, MassConverter as MassConverter, PowerConverter as PowerConverter, PressureConverter as PressureConverter, SpeedConverter as SpeedConverter, TemperatureConverter as TemperatureConverter, UnitlessRatioConverter as UnitlessRatioConverter, VolumeConverter as VolumeConverter
from sqlalchemy import Select as Select
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import Session as Session
from sqlalchemy.sql.lambdas import StatementLambdaElement as StatementLambdaElement
from statistics import mean
from typing import Any, Literal, TypedDict

QUERY_STATISTICS: Incomplete
QUERY_STATISTICS_SHORT_TERM: Incomplete
QUERY_STATISTICS_SUMMARY_MEAN: Incomplete
QUERY_STATISTICS_SUMMARY_SUM: Incomplete
STATISTIC_UNIT_TO_UNIT_CONVERTER: dict[str | None, type[BaseUnitConverter]]
DATA_SHORT_TERM_STATISTICS_RUN_CACHE: str
_LOGGER: Incomplete

class ShortTermStatisticsRunCache:
    _latest_id_by_metadata_id: dict[int, int]
    def get_latest_ids(self, metadata_ids: set[int]) -> dict[int, int]: ...
    def set_latest_id_for_metadata_id(self, metadata_id: int, id_: int) -> None: ...
    def set_latest_ids_for_metadata_ids(self, metadata_id_to_id: dict[int, int]) -> None: ...
    def __init__(self, _latest_id_by_metadata_id) -> None: ...

class BaseStatisticsRow(TypedDict, total=False):
    start: float

class StatisticsRow(BaseStatisticsRow, total=False):
    end: float
    last_reset: float | None
    state: float | None
    sum: float | None
    min: float | None
    max: float | None
    mean: float | None
    change: float | None

def _get_unit_class(unit: str | None) -> str | None: ...
def get_display_unit(hass: HomeAssistant, statistic_id: str, statistic_unit: str | None) -> str | None: ...
def _get_statistic_to_display_unit_converter(statistic_unit: str | None, state_unit: str | None, requested_units: dict[str, str] | None) -> Callable[[float | None], float | None] | None: ...
def _get_display_to_statistic_unit_converter(display_unit: str | None, statistic_unit: str | None) -> Callable[[float], float] | None: ...
def _get_unit_converter(from_unit: str, to_unit: str) -> Callable[[float | None], float | None] | None: ...
def can_convert_units(from_unit: str | None, to_unit: str | None) -> bool: ...

class PlatformCompiledStatistics:
    platform_stats: list[StatisticResult]
    current_metadata: dict[str, tuple[int, StatisticMetaData]]
    def __init__(self, platform_stats, current_metadata) -> None: ...

def split_statistic_id(entity_id: str) -> list[str]: ...

VALID_STATISTIC_ID: Incomplete

def valid_statistic_id(statistic_id: str) -> bool: ...
def validate_statistic_id(value: str) -> str: ...

class ValidationIssue:
    type: str
    data: dict[str, str | None] | None
    def as_dict(self) -> dict: ...
    def __init__(self, type, data) -> None: ...

def get_start_time() -> datetime: ...
def _compile_hourly_statistics_summary_mean_stmt(start_time_ts: float, end_time_ts: float) -> StatementLambdaElement: ...
def _compile_hourly_statistics_last_sum_stmt(start_time_ts: float, end_time_ts: float) -> StatementLambdaElement: ...
def _compile_hourly_statistics(session: Session, start: datetime) -> None: ...
def compile_missing_statistics(instance: Recorder) -> bool: ...
def compile_statistics(instance: Recorder, start: datetime, fire_events: bool) -> bool: ...
def _get_first_id_stmt(start: datetime) -> StatementLambdaElement: ...
def _compile_statistics(instance: Recorder, session: Session, start: datetime, fire_events: bool) -> set[str]: ...
def _adjust_sum_statistics(session: Session, table: type[StatisticsBase], metadata_id: int, start_time: datetime, adj: float) -> None: ...
def _insert_statistics(session: Session, table: type[StatisticsBase], metadata_id: int, statistic: StatisticData) -> StatisticsBase | None: ...
def _update_statistics(session: Session, table: type[StatisticsBase], stat_id: int, statistic: StatisticData) -> None: ...
def get_metadata_with_session(instance: Recorder, session: Session, *, statistic_ids: set[str] | None = ..., statistic_type: Literal['mean'] | Literal['sum'] | None = ..., statistic_source: str | None = ...) -> dict[str, tuple[int, StatisticMetaData]]: ...
def get_metadata(hass: HomeAssistant, *, statistic_ids: set[str] | None = ..., statistic_type: Literal['mean'] | Literal['sum'] | None = ..., statistic_source: str | None = ...) -> dict[str, tuple[int, StatisticMetaData]]: ...
def clear_statistics(instance: Recorder, statistic_ids: list[str]) -> None: ...
def update_statistics_metadata(instance: Recorder, statistic_id: str, new_statistic_id: str | None | UndefinedType, new_unit_of_measurement: str | None | UndefinedType) -> None: ...
async def async_list_statistic_ids(hass: HomeAssistant, statistic_ids: set[str] | None = ..., statistic_type: Literal['mean'] | Literal['sum'] | None = ...) -> list[dict]: ...
def _statistic_by_id_from_metadata(hass: HomeAssistant, metadata: dict[str, tuple[int, StatisticMetaData]]) -> dict[str, dict[str, Any]]: ...
def _flatten_list_statistic_ids_metadata_result(result: dict[str, dict[str, Any]]) -> list[dict]: ...
def list_statistic_ids(hass: HomeAssistant, statistic_ids: set[str] | None = ..., statistic_type: Literal['mean'] | Literal['sum'] | None = ...) -> list[dict]: ...
def _reduce_statistics(stats: dict[str, list[StatisticsRow]], same_period: Callable[[float, float], bool], period_start_end: Callable[[float], tuple[float, float]], period: timedelta, types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def reduce_day_ts_factory() -> tuple[Callable[[float, float], bool], Callable[[float], tuple[float, float]]]: ...
def _reduce_statistics_per_day(stats: dict[str, list[StatisticsRow]], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def reduce_week_ts_factory() -> tuple[Callable[[float, float], bool], Callable[[float], tuple[float, float]]]: ...
def _reduce_statistics_per_week(stats: dict[str, list[StatisticsRow]], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def _find_month_end_time(timestamp: datetime) -> datetime: ...
def reduce_month_ts_factory() -> tuple[Callable[[float, float], bool], Callable[[float], tuple[float, float]]]: ...
def _reduce_statistics_per_month(stats: dict[str, list[StatisticsRow]], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def _generate_statistics_during_period_stmt(start_time: datetime, end_time: datetime | None, metadata_ids: list[int] | None, table: type[StatisticsBase], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> StatementLambdaElement: ...
def _generate_max_mean_min_statistic_in_sub_period_stmt(columns: Select, start_time: datetime | None, end_time: datetime | None, table: type[StatisticsBase], metadata_id: int) -> StatementLambdaElement: ...
def _get_max_mean_min_statistic_in_sub_period(session: Session, result: dict[str, float], start_time: datetime | None, end_time: datetime | None, table: type[StatisticsBase], types: set[Literal['max', 'mean', 'min', 'change']], metadata_id: int) -> None: ...
def _get_max_mean_min_statistic(session: Session, head_start_time: datetime | None, head_end_time: datetime | None, main_start_time: datetime | None, main_end_time: datetime | None, tail_start_time: datetime | None, tail_end_time: datetime | None, tail_only: bool, metadata_id: int, types: set[Literal['max', 'mean', 'min', 'change']]) -> dict[str, float | None]: ...
def _first_statistic(session: Session, table: type[StatisticsBase], metadata_id: int) -> datetime | None: ...
def _get_oldest_sum_statistic(session: Session, head_start_time: datetime | None, main_start_time: datetime | None, tail_start_time: datetime | None, oldest_stat: datetime | None, tail_only: bool, metadata_id: int) -> float | None: ...
def _get_newest_sum_statistic(session: Session, head_start_time: datetime | None, head_end_time: datetime | None, main_start_time: datetime | None, main_end_time: datetime | None, tail_start_time: datetime | None, tail_end_time: datetime | None, tail_only: bool, metadata_id: int) -> float | None: ...
def statistic_during_period(hass: HomeAssistant, start_time: datetime | None, end_time: datetime | None, statistic_id: str, types: set[Literal['max', 'mean', 'min', 'change']] | None, units: dict[str, str] | None) -> dict[str, Any]: ...

_type_column_mapping: Incomplete

def _generate_select_columns_for_types_stmt(table: type[StatisticsBase], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> StatementLambdaElement: ...
def _extract_metadata_and_discard_impossible_columns(metadata: dict[str, tuple[int, StatisticMetaData]], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> list[int]: ...
def _augment_result_with_change(hass: HomeAssistant, session: Session, start_time: datetime, units: dict[str, str] | None, _types: set[Literal['change', 'last_reset', 'max', 'mean', 'min', 'state', 'sum']], table: type[Statistics | StatisticsShortTerm], metadata: dict[str, tuple[int, StatisticMetaData]], result: dict[str, list[StatisticsRow]]) -> None: ...
def _statistics_during_period_with_session(hass: HomeAssistant, session: Session, start_time: datetime, end_time: datetime | None, statistic_ids: set[str] | None, period: Literal['5minute', 'day', 'hour', 'week', 'month'], units: dict[str, str] | None, _types: set[Literal['change', 'last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def statistics_during_period(hass: HomeAssistant, start_time: datetime, end_time: datetime | None, statistic_ids: set[str] | None, period: Literal['5minute', 'day', 'hour', 'week', 'month'], units: dict[str, str] | None, types: set[Literal['change', 'last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def _get_last_statistics_stmt(metadata_id: int, number_of_stats: int) -> StatementLambdaElement: ...
def _get_last_statistics_short_term_stmt(metadata_id: int, number_of_stats: int) -> StatementLambdaElement: ...
def _get_last_statistics(hass: HomeAssistant, number_of_stats: int, statistic_id: str, convert_units: bool, table: type[StatisticsBase], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def get_last_statistics(hass: HomeAssistant, number_of_stats: int, statistic_id: str, convert_units: bool, types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def get_last_short_term_statistics(hass: HomeAssistant, number_of_stats: int, statistic_id: str, convert_units: bool, types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def get_latest_short_term_statistics_by_ids(session: Session, ids: Iterable[int]) -> list[Row]: ...
def _latest_short_term_statistics_by_ids_stmt(ids: Iterable[int]) -> StatementLambdaElement: ...
def get_latest_short_term_statistics(hass: HomeAssistant, statistic_ids: set[str], types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']], metadata: dict[str, tuple[int, StatisticMetaData]] | None = ...) -> dict[str, list[StatisticsRow]]: ...
def _generate_statistics_at_time_stmt(table: type[StatisticsBase], metadata_ids: set[int], start_time_ts: float, types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> StatementLambdaElement: ...
def _statistics_at_time(session: Session, metadata_ids: set[int], table: type[StatisticsBase], start_time: datetime, types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> Sequence[Row] | None: ...
def _fast_build_sum_list(stats_list: list[Row], table_duration_seconds: float, convert: Callable | None, start_ts_idx: int, sum_idx: int) -> list[StatisticsRow]: ...
def _sorted_statistics_to_dict(hass: HomeAssistant, session: Session, stats: Sequence[Row[Any]], statistic_ids: set[str] | None, _metadata: dict[str, tuple[int, StatisticMetaData]], convert_units: bool, table: type[StatisticsBase], start_time: datetime | None, units: dict[str, str] | None, types: set[Literal['last_reset', 'max', 'mean', 'min', 'state', 'sum']]) -> dict[str, list[StatisticsRow]]: ...
def validate_statistics(hass: HomeAssistant) -> dict[str, list[ValidationIssue]]: ...
def _statistics_exists(session: Session, table: type[StatisticsBase], metadata_id: int, start: datetime) -> int | None: ...
def _async_import_statistics(hass: HomeAssistant, metadata: StatisticMetaData, statistics: Iterable[StatisticData]) -> None: ...
def async_import_statistics(hass: HomeAssistant, metadata: StatisticMetaData, statistics: Iterable[StatisticData]) -> None: ...
def async_add_external_statistics(hass: HomeAssistant, metadata: StatisticMetaData, statistics: Iterable[StatisticData]) -> None: ...
def _filter_unique_constraint_integrity_error(instance: Recorder) -> Callable[[Exception], bool]: ...
def _import_statistics_with_session(instance: Recorder, session: Session, metadata: StatisticMetaData, statistics: Iterable[StatisticData], table: type[StatisticsBase]) -> bool: ...
def get_short_term_statistics_run_cache(hass: HomeAssistant) -> ShortTermStatisticsRunCache: ...
def cache_latest_short_term_statistic_id_for_metadata_id(run_cache: ShortTermStatisticsRunCache, session: Session, metadata_id: int) -> int | None: ...
def _find_latest_short_term_statistic_for_metadata_id_stmt(metadata_id: int) -> StatementLambdaElement: ...
def import_statistics(instance: Recorder, metadata: StatisticMetaData, statistics: Iterable[StatisticData], table: type[StatisticsBase]) -> bool: ...
def adjust_statistics(instance: Recorder, statistic_id: str, start_time: datetime, sum_adjustment: float, adjustment_unit: str) -> bool: ...
def _change_statistics_unit_for_table(session: Session, table: type[StatisticsBase], metadata_id: int, convert: Callable[[float | None], float | None]) -> None: ...
def change_statistics_unit(instance: Recorder, statistic_id: str, new_unit: str, old_unit: str) -> None: ...
def async_change_statistics_unit(hass: HomeAssistant, statistic_id: str, *, new_unit_of_measurement: str, old_unit_of_measurement: str) -> None: ...
def cleanup_statistics_timestamp_migration(instance: Recorder) -> bool: ...
