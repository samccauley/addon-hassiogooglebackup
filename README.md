# Backup to Google Drive
## Overview
This add-on will upload files from your hass[]().io backup folder (typically .tar files created by the hass[]().io SnapShot feature) to your Google Drive. A few key things to note:
1. This add-on asks only for permission to add new files to your Google Drive, and to manage the files that it adds. It will not have permission to view any files on your Google Drive that it did not create itself. This is to protect the contents of your Google Drive.
2. This add-on exposes a Web User Interface for obtaining your authorization to upload files to your Google Drive. Once that authorization is established, the Web User Interface is no longer needed - it exists only for this initial setup.
3. Backups are performed by executing a REST service exposed on the same port as the Web User Interface. Find [more information on the service below](Calling-the-`doBackup`-Service). You can use [Home Assistant's RESTful Command](https://www.home-assistant.io/components/rest_command/) to integrate this add-on's REST service into your own scripts and automations.
## Configuration Options
Example configuration:
```
{"copyFromFilter" : "/backup/*.tar",
 "backupToDir" : "8579ED8"}
```
### `copyFromFilter`
Use this to identify the files on your hass[]().io host that you wish to backup.

This filter is used to identify a list of files to backup. That list is then pared down by checking Google Drive to see if any files in the list have already been backed up by this add-on. This check is performed to avoid backing up the same file twice (Google Drive allows duplicate files with the same name).

    Note that this add-on can only see files on your Google Drive that it created itself. Therefore, if you have backed up some of your snapshots on your own to Google Drive, this add-on will not be aware of those and it will back them up anyway.
### `backupToDir`
This identifies the Google Drive folder in which you want to place your backed up files. Because this add-on does not have permission to browse any files or directories on your Google Drive that it does not itself create, you cannot simply provide the folder name. You must instead provide Google Drive's somewhat-hidden unique ID of the folder. Google Drive doesn't make it easy to get this value. But, here's how you can get it:
1. In your favorite web browser, navigate to the Google Drive folder to which you plan to upload your files (create a new folder in Google Drive if you wish). Be sure that you have the perferred folder open so that its contents (even if it's empty) are displayed.
2. From the address bar of your browser, copy the last portion of the URL. That value is Google Drive's unique ID for the folder. Paste that value in for the `backupToDir` value in the configuration.
## Authorizing this Add-On to Upload to Google Drive

## Calling the `doBackup` Service
