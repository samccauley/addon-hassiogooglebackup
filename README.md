# Backup to Google Drive
![Backup to Google Drive Logo](logo.png "Backup to Google Drive Logo")
## Overview
This add-on will upload files from your hass[]().io backup folder (typically .tar files created by the hass[]().io SnapShot feature) to your Google Drive. A few key things to note:
1. This add-on asks only for permission to add new files to your Google Drive, and to manage the files that it adds. It will not have permission to view any files on your Google Drive that it did not create itself. This is to protect the contents of your Google Drive.
2. This add-on exposes a Web User Interface for obtaining your authorization to upload files to your Google Drive. Once that authorization is established, the Web User Interface is no longer needed - it exists only for this initial setup.
3. Backups are performed by executing a REST service exposed on the same port as the Web User Interface. Find [more information on the service below](#Calling-the-`doBackup`-Service). You can use [Home Assistant's RESTful Command](https://www.home-assistant.io/components/rest_command/) to integrate this add-on's REST service into your own scripts and automations. You may want to use a REST testing tool like [Postman](https://www.getpostman.com/) to perform initial testing.
## Configuration Options
Example configuration:
```
{"fromPattern" : "/backup/*.tar",
 "backupDirID" : "1CvPDzNz1v-OuOUqKq3jjoKQt020hKK7R"}
```
### `fromPattern`
Use this to identify the files on your hass[]().io host that you wish to backup.

This pattern is used to identify a list of files to backup. That list is then pared down by checking Google Drive to see if any files in the list have already been backed up by this add-on. This check is performed to avoid backing up the same file twice (Google Drive allows duplicate files with the same name).

    Note that this add-on can only see files on your Google Drive that it created itself. Therefore, if you have backed up some of your snapshots on your own to Google Drive, this add-on will not be aware of those and it will back them up anyway.
### `backupDirID`
This identifies the Google Drive folder in which you want to place your backed up files. Because this add-on does not have permission to browse any files or directories on your Google Drive that it does not itself create, you cannot simply provide the folder name. You must instead provide Google Drive's unique opaque ID of the folder. Google Drive doesn't make it easy to get this value. But, here's how you can get it:
1. In your favorite web browser, navigate to the Google Drive folder to which you plan to upload your files (create a new folder in Google Drive if you wish). Be sure that you have the perferred folder open so that its contents (even if it's empty) are displayed.
2. From the address bar of your browser, copy the last portion of the URL. That value is Google Drive's unique opaque ID for the folder. Paste that value in for the `backupDirID` value in the configuration.
## Authorizing this Add-On to Upload to Google Drive
This add-on requires you to authorize it to a limited scope of access to your Google Drive. This specific scope it requires is `https://www.googleapis.com/auth/drive.file`. You can read information about what that scope entails in [Google's Guide to OAuth 2.0 Scopes](https://developers.google.com/identity/protocols/googlescopes). Essentially, it allows this add-on to view and manage Google Drive files and folders that you have opened or created with this add-on.

Before using the [`doBackup` Service](Calling-the-`doBackup`-Service), you need to follow these steps to grant this add-on the required authorization:
1. Start this add-on and make sure that it is set to `Start on boot`.
2. Open the Web User Interface for this add-on using the `Open Web UI` link on the add-on details page. Alternatively, you can open your own browser window and navigate to: `http://<Your_Hassio_Host>:<Host_Port>/gb`, substituting your hass[]().io host name and the Host Port number you've configured for this add-on.
3. Following the instructions in the Web User Interface, do the following:
    1. Click on the `AUTHORIZE` button to launch a separate browser tab to the Google Authorization Server.
    2. If required, login to Google and confirm your Google user ID.
    3. Google will then tell you what application (this add-on) is requesting authority and what scope of authority is being requested. Click Google's `Allow` button.
    4. Google will then show you an authorization code. Copy this code so that you can paste into this add-on's Web User Interface (next step).
    5. Return to the browser tab containing this add-on's Web User Interface and paste the copied value (from the previous step) into the provided `Authorization Code' field.
    6. Click the `INGEST CODE` button.
    7. You should be presented with a message indicating **authorization received**.
4. This completes the authorization step! You're now ready to begin using the `doBackup` Service as described below.
## Calling the `doBackup` Service
Backups are performed by calling the `doBackup` service exposed by this add-on. When you start this add-on, the service becomes available on the Host Port that you've configured this add-on to use.

The `doBackup` service does not require any arguments. It gets the information it needs from the [Configuration Options](#Configuration-Options) and from your having completed the [authorization process described above](#Authorizing-this-Add-On-to-Upload-to-Google-Drive).

You call the service by simply performing a GET against this URI:
```
    http://<YOUR_HASSIO_HOST>:<HOST_PORT>/gb/doBackup
```
Substitute in your hass[]().io host name (usually `hassio.local`) and the Host Port number you've configured for this add-on.

The `doBackup` service will respond with JSON reminding you of the configuration settings that it used and indicating:
- how many files were found using the `copyFromFilter`
- how many of those files had alredy been backed up to your Google Drive and were therfore skipped this time
- how many files the `doBackup` service actually backed up during this run

### Sample JSON Response
```
{
    "fromPattern": "/backup/*.tar",
    "backupDirID": "1CvPDzNz1v-OuOUqKq3jjoKQt020hKK7R",
    "fileCount": 5,
    "alreadyCount": 2,
    "backedUpCount": 3
}
```
Unexpected errors will return an HTTP Status Code of some value other than the normal 200 Success Code.