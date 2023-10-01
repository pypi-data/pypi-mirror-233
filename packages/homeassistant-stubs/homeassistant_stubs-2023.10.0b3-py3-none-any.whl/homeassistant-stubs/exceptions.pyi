from .core import Context as Context
from _typeshed import Incomplete
from collections.abc import Generator, Sequence

class HomeAssistantError(Exception): ...
class InvalidEntityFormatError(HomeAssistantError): ...
class NoEntitySpecifiedError(HomeAssistantError): ...

class TemplateError(HomeAssistantError):
    def __init__(self, exception: Exception | str) -> None: ...

class ConditionError(HomeAssistantError):
    type: str
    @staticmethod
    def _indent(indent: int, message: str) -> str: ...
    def output(self, indent: int) -> Generator[str, None, None]: ...
    def __str__(self) -> str: ...
    def __init__(self, type) -> None: ...

class ConditionErrorMessage(ConditionError):
    message: str
    def output(self, indent: int) -> Generator[str, None, None]: ...
    def __init__(self, type, message) -> None: ...

class ConditionErrorIndex(ConditionError):
    index: int
    total: int
    error: ConditionError
    def output(self, indent: int) -> Generator[str, None, None]: ...
    def __init__(self, type, index, total, error) -> None: ...

class ConditionErrorContainer(ConditionError):
    errors: Sequence[ConditionError]
    def output(self, indent: int) -> Generator[str, None, None]: ...
    def __init__(self, type, errors) -> None: ...

class IntegrationError(HomeAssistantError):
    def __str__(self) -> str: ...

class PlatformNotReady(IntegrationError): ...
class ConfigEntryError(IntegrationError): ...
class ConfigEntryNotReady(IntegrationError): ...
class ConfigEntryAuthFailed(IntegrationError): ...
class InvalidStateError(HomeAssistantError): ...

class Unauthorized(HomeAssistantError):
    context: Incomplete
    user_id: Incomplete
    entity_id: Incomplete
    config_entry_id: Incomplete
    perm_category: Incomplete
    permission: Incomplete
    def __init__(self, context: Context | None = ..., user_id: str | None = ..., entity_id: str | None = ..., config_entry_id: str | None = ..., perm_category: str | None = ..., permission: str | None = ...) -> None: ...

class UnknownUser(Unauthorized): ...

class ServiceNotFound(HomeAssistantError):
    domain: Incomplete
    service: Incomplete
    def __init__(self, domain: str, service: str) -> None: ...
    def __str__(self) -> str: ...

class MaxLengthExceeded(HomeAssistantError):
    value: Incomplete
    property_name: Incomplete
    max_length: Incomplete
    def __init__(self, value: str, property_name: str, max_length: int) -> None: ...

class DependencyError(HomeAssistantError):
    failed_dependencies: Incomplete
    def __init__(self, failed_dependencies: list[str]) -> None: ...
