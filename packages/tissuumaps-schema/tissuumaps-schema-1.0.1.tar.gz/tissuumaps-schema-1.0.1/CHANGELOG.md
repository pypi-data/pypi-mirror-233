# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.1](https://github.com/TissUUmaps/TissUUmaps-schema/compare/v1.0.0...v1.0.1)

### Fixed
- Bug in `models` command

### Changed
- Versioning scheme: PATCH indicates Python package bugfixes (removed PATCH from schema versioning)


## [v1.0.0](https://github.com/TissUUmaps/TissUUmaps-schema/compare/v0.1.0...v1.0.0)

### Added
- Schema version 0.1.0 ("expectedCSV" format of an EOL TissUUmaps version)
- Upgrade path from schema version 0.1.0 to schema version 1.0.0

### Fixed
- Class hierarchy
- Bug in `upgrade` command
- Version inference in `validate` command
- Typing and/or default values of:
    - Setting.value (type: int|float -> Any)
    - ExpectedHeader.collectionItem_fixed (type: str -> str|int; default: "" -> 0)
    - ExpectedRadios.collectionItem_fixed (default: False -> True)

### Changed
- Renamed schema version 0.1 to schema version 1.0.0

### Removed


## [v0.1.0](https://github.com/TissUUmaps/TissUUmaps-schema/releases/tag/v0.1.0)

Initial release
