import asyncio
import threading
from . import migration as migration, statistics as statistics
from .const import CONTEXT_ID_AS_BINARY_SCHEMA_VERSION as CONTEXT_ID_AS_BINARY_SCHEMA_VERSION, DB_WORKER_PREFIX as DB_WORKER_PREFIX, DOMAIN as DOMAIN, ESTIMATED_QUEUE_ITEM_SIZE as ESTIMATED_QUEUE_ITEM_SIZE, EVENT_TYPE_IDS_SCHEMA_VERSION as EVENT_TYPE_IDS_SCHEMA_VERSION, KEEPALIVE_TIME as KEEPALIVE_TIME, LEGACY_STATES_EVENT_ID_INDEX_SCHEMA_VERSION as LEGACY_STATES_EVENT_ID_INDEX_SCHEMA_VERSION, MARIADB_PYMYSQL_URL_PREFIX as MARIADB_PYMYSQL_URL_PREFIX, MARIADB_URL_PREFIX as MARIADB_URL_PREFIX, MAX_QUEUE_BACKLOG_MIN_VALUE as MAX_QUEUE_BACKLOG_MIN_VALUE, MYSQLDB_PYMYSQL_URL_PREFIX as MYSQLDB_PYMYSQL_URL_PREFIX, MYSQLDB_URL_PREFIX as MYSQLDB_URL_PREFIX, QUEUE_PERCENTAGE_ALLOWED_AVAILABLE_MEMORY as QUEUE_PERCENTAGE_ALLOWED_AVAILABLE_MEMORY, SQLITE_URL_PREFIX as SQLITE_URL_PREFIX, STATES_META_SCHEMA_VERSION as STATES_META_SCHEMA_VERSION, STATISTICS_ROWS_SCHEMA_VERSION as STATISTICS_ROWS_SCHEMA_VERSION, SupportedDialect as SupportedDialect
from .db_schema import Base as Base, EventData as EventData, EventTypes as EventTypes, Events as Events, LEGACY_STATES_ENTITY_ID_LAST_UPDATED_INDEX as LEGACY_STATES_ENTITY_ID_LAST_UPDATED_INDEX, LEGACY_STATES_EVENT_ID_INDEX as LEGACY_STATES_EVENT_ID_INDEX, SCHEMA_VERSION as SCHEMA_VERSION, StateAttributes as StateAttributes, States as States, StatesMeta as StatesMeta, Statistics as Statistics, StatisticsShortTerm as StatisticsShortTerm, TABLE_STATES as TABLE_STATES
from .executor import DBInterruptibleThreadPoolExecutor as DBInterruptibleThreadPoolExecutor
from .models import DatabaseEngine as DatabaseEngine, StatisticData as StatisticData, StatisticMetaData as StatisticMetaData, UnsupportedDialect as UnsupportedDialect
from .pool import MutexPool as MutexPool, POOL_SIZE as POOL_SIZE, RecorderPool as RecorderPool
from .queries import has_entity_ids_to_migrate as has_entity_ids_to_migrate, has_event_type_to_migrate as has_event_type_to_migrate, has_events_context_ids_to_migrate as has_events_context_ids_to_migrate, has_states_context_ids_to_migrate as has_states_context_ids_to_migrate
from .table_managers.event_data import EventDataManager as EventDataManager
from .table_managers.event_types import EventTypeManager as EventTypeManager
from .table_managers.recorder_runs import RecorderRunsManager as RecorderRunsManager
from .table_managers.state_attributes import StateAttributesManager as StateAttributesManager
from .table_managers.states import StatesManager as StatesManager
from .table_managers.states_meta import StatesMetaManager as StatesMetaManager
from .table_managers.statistics_meta import StatisticsMetaManager as StatisticsMetaManager
from .tasks import AdjustLRUSizeTask as AdjustLRUSizeTask, AdjustStatisticsTask as AdjustStatisticsTask, ChangeStatisticsUnitTask as ChangeStatisticsUnitTask, ClearStatisticsTask as ClearStatisticsTask, CommitTask as CommitTask, CompileMissingStatisticsTask as CompileMissingStatisticsTask, DatabaseLockTask as DatabaseLockTask, EntityIDMigrationTask as EntityIDMigrationTask, EntityIDPostMigrationTask as EntityIDPostMigrationTask, EventIdMigrationTask as EventIdMigrationTask, EventTask as EventTask, EventTypeIDMigrationTask as EventTypeIDMigrationTask, EventsContextIDMigrationTask as EventsContextIDMigrationTask, ImportStatisticsTask as ImportStatisticsTask, KeepAliveTask as KeepAliveTask, PerodicCleanupTask as PerodicCleanupTask, PurgeTask as PurgeTask, RecorderTask as RecorderTask, StatesContextIDMigrationTask as StatesContextIDMigrationTask, StatisticsTask as StatisticsTask, StopTask as StopTask, SynchronizeTask as SynchronizeTask, UpdateStatesMetadataTask as UpdateStatesMetadataTask, UpdateStatisticsMetadataTask as UpdateStatisticsMetadataTask, WaitTask as WaitTask
from .util import build_mysqldb_conv as build_mysqldb_conv, dburl_to_path as dburl_to_path, end_incomplete_runs as end_incomplete_runs, execute_stmt_lambda_element as execute_stmt_lambda_element, get_index_by_name as get_index_by_name, is_second_sunday as is_second_sunday, move_away_broken_database as move_away_broken_database, session_scope as session_scope, setup_connection_for_dialect as setup_connection_for_dialect, validate_or_move_away_sqlite_database as validate_or_move_away_sqlite_database, write_lock_db_sqlite as write_lock_db_sqlite
from _typeshed import Incomplete
from collections.abc import Callable as Callable, Iterable
from datetime import datetime
from homeassistant.components import persistent_notification as persistent_notification
from homeassistant.const import ATTR_ENTITY_ID as ATTR_ENTITY_ID, EVENT_HOMEASSISTANT_CLOSE as EVENT_HOMEASSISTANT_CLOSE, EVENT_HOMEASSISTANT_FINAL_WRITE as EVENT_HOMEASSISTANT_FINAL_WRITE, EVENT_STATE_CHANGED as EVENT_STATE_CHANGED, MATCH_ALL as MATCH_ALL
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, Event as Event, HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.event import async_track_time_change as async_track_time_change, async_track_time_interval as async_track_time_interval, async_track_utc_time_change as async_track_utc_time_change
from homeassistant.helpers.start import async_at_started as async_at_started
from homeassistant.helpers.typing import UNDEFINED as UNDEFINED, UndefinedType as UndefinedType
from homeassistant.util.enum import try_parse_enum as try_parse_enum
from sqlalchemy.engine import Engine as Engine
from sqlalchemy.engine.interfaces import DBAPIConnection as DBAPIConnection
from sqlalchemy.orm.session import Session as Session
from typing import Any, TypeVar

_LOGGER: Incomplete
T = TypeVar('T')
DEFAULT_URL: str
EXPIRE_AFTER_COMMITS: int
SHUTDOWN_TASK: Incomplete
COMMIT_TASK: Incomplete
KEEP_ALIVE_TASK: Incomplete
WAIT_TASK: Incomplete
ADJUST_LRU_SIZE_TASK: Incomplete
DB_LOCK_TIMEOUT: int
DB_LOCK_QUEUE_CHECK_TIMEOUT: int
INVALIDATED_ERR: str
CONNECTIVITY_ERR: str
MAX_DB_EXECUTOR_WORKERS: Incomplete

class Recorder(threading.Thread):
    stop_requested: bool
    hass: Incomplete
    thread_id: Incomplete
    auto_purge: Incomplete
    auto_repack: Incomplete
    keep_days: Incomplete
    _hass_started: Incomplete
    commit_interval: Incomplete
    _queue: Incomplete
    db_url: Incomplete
    db_max_retries: Incomplete
    db_retry_wait: Incomplete
    database_engine: Incomplete
    async_db_connected: Incomplete
    async_db_ready: Incomplete
    async_recorder_ready: Incomplete
    _queue_watch: Incomplete
    engine: Incomplete
    max_backlog: Incomplete
    _psutil: Incomplete
    entity_filter: Incomplete
    exclude_event_types: Incomplete
    schema_version: int
    _commits_without_expire: int
    _event_session_has_pending_writes: bool
    recorder_runs_manager: Incomplete
    states_manager: Incomplete
    event_data_manager: Incomplete
    event_type_manager: Incomplete
    states_meta_manager: Incomplete
    state_attributes_manager: Incomplete
    statistics_meta_manager: Incomplete
    event_session: Incomplete
    _get_session: Incomplete
    _completed_first_database_setup: Incomplete
    async_migration_event: Incomplete
    migration_in_progress: bool
    migration_is_live: bool
    use_legacy_events_index: bool
    _database_lock_task: Incomplete
    _db_executor: Incomplete
    _event_listener: Incomplete
    _queue_watcher: Incomplete
    _keep_alive_listener: Incomplete
    _commit_listener: Incomplete
    _periodic_listener: Incomplete
    _nightly_listener: Incomplete
    _dialect_name: Incomplete
    enabled: bool
    def __init__(self, hass: HomeAssistant, auto_purge: bool, auto_repack: bool, keep_days: int, commit_interval: int, uri: str, db_max_retries: int, db_retry_wait: int, entity_filter: Callable[[str], bool], exclude_event_types: set[str]) -> None: ...
    @property
    def backlog(self) -> int: ...
    @property
    def dialect_name(self) -> SupportedDialect | None: ...
    @property
    def _using_file_sqlite(self) -> bool: ...
    @property
    def recording(self) -> bool: ...
    def get_session(self) -> Session: ...
    def queue_task(self, task: RecorderTask) -> None: ...
    def set_enable(self, enable: bool) -> None: ...
    def async_start_executor(self) -> None: ...
    def _shutdown_pool(self) -> None: ...
    def async_initialize(self) -> None: ...
    def _async_keep_alive(self, now: datetime) -> None: ...
    def _async_commit(self, now: datetime) -> None: ...
    def async_add_executor_job(self, target: Callable[..., T], *args: Any) -> asyncio.Future[T]: ...
    def _stop_executor(self) -> None: ...
    def _async_check_queue(self, *_: Any) -> None: ...
    def _available_memory(self) -> int: ...
    def _reached_max_backlog_percentage(self, percentage: int) -> bool: ...
    def _async_stop_queue_watcher_and_event_listener(self) -> None: ...
    def _async_stop_listeners(self) -> None: ...
    async def _async_close(self, event: Event) -> None: ...
    async def _async_shutdown(self, event: Event) -> None: ...
    def _async_hass_started(self, hass: HomeAssistant) -> None: ...
    def async_register(self) -> None: ...
    def _async_startup_failed(self) -> None: ...
    def async_connection_success(self) -> None: ...
    def async_set_db_ready(self) -> None: ...
    def _async_set_recorder_ready_migration_done(self) -> None: ...
    def async_nightly_tasks(self, now: datetime) -> None: ...
    def _async_five_minute_tasks(self, now: datetime) -> None: ...
    def _adjust_lru_size(self) -> None: ...
    def async_periodic_statistics(self) -> None: ...
    def async_adjust_statistics(self, statistic_id: str, start_time: datetime, sum_adjustment: float, adjustment_unit: str) -> None: ...
    def async_clear_statistics(self, statistic_ids: list[str]) -> None: ...
    def async_update_statistics_metadata(self, statistic_id: str, *, new_statistic_id: str | UndefinedType = ..., new_unit_of_measurement: str | None | UndefinedType = ...) -> None: ...
    def async_update_states_metadata(self, entity_id: str, new_entity_id: str) -> None: ...
    def async_change_statistics_unit(self, statistic_id: str, *, new_unit_of_measurement: str, old_unit_of_measurement: str) -> None: ...
    def async_import_statistics(self, metadata: StatisticMetaData, stats: Iterable[StatisticData], table: type[Statistics | StatisticsShortTerm]) -> None: ...
    def _async_setup_periodic_tasks(self) -> None: ...
    async def _async_wait_for_started(self) -> object | None: ...
    def _wait_startup_or_shutdown(self) -> object | None: ...
    def run(self) -> None: ...
    def _add_to_session(self, session: Session, obj: object) -> None: ...
    def _run(self) -> None: ...
    def _activate_and_set_db_ready(self) -> None: ...
    def _run_event_loop(self) -> None: ...
    def _pre_process_startup_tasks(self, startup_tasks: list[RecorderTask]) -> None: ...
    def _guarded_process_one_task_or_recover(self, task: RecorderTask) -> None: ...
    def _process_one_task_or_recover(self, task: RecorderTask) -> None: ...
    def _setup_recorder(self) -> bool: ...
    def _async_migration_started(self) -> None: ...
    def _migrate_schema_and_setup_run(self, schema_status: migration.SchemaValidationStatus) -> bool: ...
    def _lock_database(self, task: DatabaseLockTask) -> None: ...
    def _process_one_event(self, event: Event) -> None: ...
    def _process_non_state_changed_event_into_session(self, event: Event) -> None: ...
    def _process_state_changed_event_into_session(self, event: Event) -> None: ...
    def _handle_database_error(self, err: Exception) -> bool: ...
    def _commit_event_session_or_retry(self) -> None: ...
    def _commit_event_session(self) -> None: ...
    def _handle_sqlite_corruption(self) -> None: ...
    def _close_event_session(self) -> None: ...
    def _reopen_event_session(self) -> None: ...
    def _open_event_session(self) -> None: ...
    def _post_schema_migration(self, old_version: int, new_version: int) -> None: ...
    def _migrate_states_context_ids(self) -> bool: ...
    def _migrate_events_context_ids(self) -> bool: ...
    def _migrate_event_type_ids(self) -> bool: ...
    def _migrate_entity_ids(self) -> bool: ...
    def _post_migrate_entity_ids(self) -> bool: ...
    def _cleanup_legacy_states_event_ids(self) -> bool: ...
    def _send_keep_alive(self) -> None: ...
    async def async_block_till_done(self) -> None: ...
    def block_till_done(self) -> None: ...
    async def lock_database(self) -> bool: ...
    def unlock_database(self) -> bool: ...
    def _setup_recorder_connection(self, dbapi_connection: DBAPIConnection, connection_record: Any) -> None: ...
    def _setup_connection(self) -> None: ...
    def _close_connection(self) -> None: ...
    def _setup_run(self) -> None: ...
    def _schedule_compile_missing_statistics(self) -> None: ...
    def _end_session(self) -> None: ...
    def _shutdown(self) -> None: ...
