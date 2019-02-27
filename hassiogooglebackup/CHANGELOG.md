# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.2] - 2019-02-27
### Fixed
- Changed to use Python base build

## [1.5.1] - 2019-02-19
### Fixed
- Changed MQTT topic from retain=True to retain=False.

## [1.5.0] - 2019-02-18
### Added
- Now publishing result JSON object as an MQTT event.
### Fixed
- Built using latest version of hass[]()io builder in hope to eliminate seqmentation fault being experienced by some users. 

## [1.4.0] - 2019-02-14
### Added
- Improved logging and added option to run in DEBUG mode.
### Fixed
- Upgraded Django from 2.1.2 to 2.1.7 patching security vulnerabilities.

## [1.3.0] - 2018-11-26
### Added
- Added a backupTimestamp to the JSON returned by the doBackup service.

## [1.2.0] - 2018-11-10
### Added
- Ability to purge older snapshots from your Google Drive folder, preserving a given number of recent files.

## [1.1.0] - 2018-11-09
### Added
- Ability to purge older snapshots from your hass[]()io backup folder, preserving a given number of recent files.

## [1.0.2] - 2018-11-03
### Changed
- Added instructions to README on how to create REST Service in Home Assistant.

## [1.0.1] - 2018-11-03
### Changed
- Experimental update - ALLOWED_HOSTS - '*'

## [1.0.0] - 2018-11-02
### Added
- Initial Release with basic ability to upload snapshots to Google Drive, avoiding duplication of files previously backed up.