from typing import Any

from . import v00, v01


def guess_schema_version(model_data: dict[str, Any]) -> str:
    marker_files = model_data.get("markerFiles")
    if marker_files is not None and any(
        "expectedCSV" in marker_file for marker_file in marker_files
    ):
        return v00.VERSION
    return model_data.get("schemaVersion", v01.VERSION)


def get_major_version(version: str) -> str:
    return version.split(".")[0]


SCHEMA_MODULES = [v00, v01]

CURRENT_SCHEMA_MODULE = v01

MAJOR_SCHEMA_VERSIONS = sorted(
    get_major_version(schema_module.VERSION) for schema_module in SCHEMA_MODULES
)

MAJOR_SCHEMA_VERSION_MODULES = {
    get_major_version(schema_module.VERSION): schema_module
    for schema_module in SCHEMA_MODULES
}
