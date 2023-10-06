from .utils import CURRENT_SCHEMA_MODULE, SCHEMA_MODULES, guess_schema_version

current = CURRENT_SCHEMA_MODULE

__all__ = ["current", "guess_schema_version", "SCHEMA_MODULES"]
