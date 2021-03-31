# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.8] - 2021-03-31

### Fixed

- General code clean up and some build automation code.
- Patched httplib2 from 0.15.0 to 0.19.0
- Patched rsa from 4.0 to 4.1

## [1.7.7] - 2020-08-19

### Fixed

- Fixed to support preserving more than 100 files on Google Drive.

## [1.7.6] - 2020-06-24

### Fixed

- Pinned httplib2 to 0.15.0 to avoid breaking change triggered by Google's
non-standard way of handing redirects in their chunking logic for large file
uploads. When I upgraded httplib2 to 0.18.0 to address vulnerabilities, a
problem with redirect 308 codes was introduced. I had hoped that upgrading the
Google APIs would fix it, but it does not. So, I'm rolling back httplib2 instead.

## [1.7.5] - 2020-06-22

### Fixed

- Patched google-api-python-client to 1.9.3
- Patched google-auth to 1.18.0
- Patched google-auth-oauthlib to 0.4.1

## [1.7.4] - 2020-06-10

### Fixed

- Patched google-api-python-client to 1.7.12 per
<https://github.com/googleapis/google-api-python-client/pull/813>
to address redirect error in httplib2.

## [1.7.3] - 2020-06-07

### Fixed

- Patched Django to 2.2.13 to address vulnerability.
- Patched httplib2 to 0.18.0 to address vulnerability.

## [1.7.2] - 2020-01-18

### Fixed

- Patched Django to 2.2.9 to address vulnerability.

## [1.7.1] - 2019-09-09

### Fixed

- Fixed Gunicorn settings to support async worker threads. This is necessary
to support larger snapshots that take longer to upload to Google Drive.
I should've had it configured this way from the start in v 1.7.0.

## [1.7.0] - 2019-08-29

### Fixed

- Updated Django to 2.1.11 to address vulnerabilities
- Added Gunicorn as the web server. Previously was just using Django's
development server - not good practice, I know. I was lazy.

## [1.6.2] - 2019-06-28

### Fixed

- Updated Django to 2.1.9 and updated urllib3 to 1.24.2 to address vulnerabilities

## [1.6.1] - 2019-03-19

### Fixed

- Modified config to reduce unnecessary CPU usage.

## [1.6.0] - 2019-03-16

### New

- Added a second service operation called `adhocBackup`. This is completely
separate from the normal backup operations performed using the `doBackup`
service operation. The new adhoc backups do not rely on the pre-configured
options `fromPattern`, `backupDirID`, `purge` and `purge_google`. Instead, an
adhoc backup request identifies which files are to be backed up and which
Google Drive folder is to be targeted each time it is placed (hence the
name, "adhoc"). The concept of "purging" of older files while preserving more
recent files does not apply at all to adhoc backups. Adhoc backups simply
copy each identified file from your hassio host to your Google Drive,
**replacing the target file on Google Drive if it already exists**.

### Fixed

- Added a paragraph in the readme file providing add-on installation instructions.
- Added some additional debugging log entries - in case of emergency.

## [1.5.2] - 2019-02-27

### Fixed

- Changed to use Python base build in attempt to avoid segmentation faults
being experienced by users on 64 bit Hassos.

## [1.5.1] - 2019-02-19

### Fixed

- Changed MQTT topic from retain=True to retain=False. If you happened to
install and use version 1.5.0 of the Google Backup add-on, you will have a
retained backup result event stored in MQTT. You can remove this by using
Home Assistant's mqtt.publish service to send the following message.
This will clear out the previously retained message.
        ```{ "topic": "googlebackup/result",
          "retain": true }```

## [1.5.0] - 2019-02-18

### Added

- Now publishing result JSON object as an MQTT event.

### Fixed

- Built using latest version of hassio builder in hope to eliminate
seqmentation fault being experienced by some users.

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

- Ability to purge older snapshots from your Google Drive folder, preserving
a given number of recent files.

## [1.1.0] - 2018-11-09

### Added

- Ability to purge older snapshots from your hassio backup folder,
preserving a given number of recent files.

## [1.0.2] - 2018-11-03

### Changed

- Added instructions to README on how to create REST Service in Home Assistant.

## [1.0.1] - 2018-11-03

### Changed

- Experimental update - ALLOWED_HOSTS - '*'

## [1.0.0] - 2018-11-02

### Added

- Initial Release with basic ability to upload snapshots to Google Drive,
avoiding duplication of files previously backed up.
