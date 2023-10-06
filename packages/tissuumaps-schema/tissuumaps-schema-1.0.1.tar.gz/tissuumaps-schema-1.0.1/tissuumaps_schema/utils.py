from typing import Any

from . import v00, v01

SCHEMA_MODULES = [v00, v01]

current_schema_module = v01


def guess_schema_version(model_data: dict[str, Any]) -> str:
    marker_files = model_data.get("markerFiles")
    if marker_files is not None and any(
        "expectedCSV" in marker_file for marker_file in marker_files
    ):
        return v00.VERSION
    return model_data.get("schemaVersion", v01.VERSION)
