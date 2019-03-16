import googleapiclient.http
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from httplib2 import Http
import logging
import requests

from django.conf import settings
import os
import json
import glob
import ntpath
from pprint import pformat
import datetime
import mimetypes

OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive.file'

CLIENT_SECRET = os.path.join(settings.BASE_DIR, "client_secret.json")
TOKEN = os.path.join(settings.DATA_PATH, "token.json")
CONFIG_FILE = os.path.join(settings.DATA_PATH, "options.json")


def getOptions():
    with open(CONFIG_FILE) as f:
        options = json.load(f)
    return options

def getFlowFromClientSecret():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes=[OAUTH2_SCOPE])
    return flow

def getFlowFromClientSecret_Step2(saved_state):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes=[OAUTH2_SCOPE],
        state=saved_state)
    return flow

def requestAuthorization():

    flow = getFlowFromClientSecret()

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required.
    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    return authorization_url, state

def fetchAndSaveTokens(saved_state, redirect_uri, authorization_response, authorizationCode):

    flow = getFlowFromClientSecret_Step2(saved_state)
    # flow.redirect_uri = redirect_uri
    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

    flow.fetch_token(code=authorizationCode)

    # Store the credentials for later use by REST service
    credentials = flow.credentials
    tokens = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    with open(TOKEN, 'w') as outfile:
        json.dump(tokens, outfile)

def getDriveService(user_agent):

    with open(TOKEN) as f:
        creds = json.load(f)

    credentials = GoogleCredentials(None,creds["client_id"],creds["client_secret"],
                                          creds["refresh_token"],None,"https://accounts.google.com/o/oauth2/token",user_agent)
    http = credentials.authorize(Http())
    credentials.refresh(http)
    drive_service = build('drive', 'v3', http)

    return drive_service

def alreadyBackedUp(fileName, backupDirID, drive_service):

    shortFileName = ntpath.basename(fileName)

    # Search for given file in Google Drive Directory
    results = drive_service.files().list(
        q="name='" + shortFileName + "' and '" + backupDirID + "' in parents and trashed = false",
        spaces='drive',
        fields="files(id, name)").execute()
    items = results.get('files', [])

    return len(items) > 0

def deleteIfThere(fileName, backupDirID, drive_service):

    shortFileName = ntpath.basename(fileName)

    logging.debug("Will delete " + shortFileName + " if it is already in Google Drive.")

    # Search for given file in Google Drive Directory
    results = drive_service.files().list(
        q="name='" + shortFileName + "' and '" + backupDirID + "' in parents and trashed = false",
        spaces='drive',
        fields="files(id, name)").execute()
    items = results.get('files', [])

    logging.debug("Found " + str(len(items)) + " files named " + shortFileName + " in Google Drive.")

    deletedCount = 0
    for file in items:
        drive_service.files().delete(fileId=file.get('id')).execute()
        deletedCount += 1
        logging.info("Deleted " + file.get('name') + " : " + file.get('id'))

    logging.info("Deleted " + str(deletedCount) + " files named " + shortFileName + " from Google Drive.")

    return deletedCount

def backupFile(fileName, backupDirID, drive_service, MIMETYPE, TITLE, DESCRIPTION):

    logging.info("Backing up " + fileName + " to " + backupDirID)

    logging.debug("drive_service = " + str(drive_service))
    logging.debug("MIMETYPE = " + MIMETYPE)
    logging.debug("TITLE = " + TITLE)
    logging.debug("DESCRIPTION = " + DESCRIPTION)

    shortFileName = ntpath.basename(fileName)

    media_body = googleapiclient.http.MediaFileUpload(
        fileName,
        mimetype=MIMETYPE,
        resumable=True
    )

    logging.debug("media_body: " + str(media_body))

    body = {
        'name': shortFileName,
        'title': TITLE,
        'description': DESCRIPTION,
        'parents': [backupDirID]
    }

    new_file = drive_service.files().create(
    body=body, media_body=media_body).execute()
    logging.debug(pformat(new_file))

def publishResult(result):
    url = settings.HA_MQTT_PUBLISH_URL
    data = {"payload" : json.dumps(result),
            "topic" : settings.HA_MQTT_RESULT_TOPIC,
            "retain" : settings.HA_MQTT_RESULT_RETAIN}
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json',
                'Authorization': 'Bearer ' + settings.HA_TOKEN}

    response = requests.post(url, data=data_json, headers=headers)
    logging.debug(pformat(response))

def publishAdhocResult(result):
    url = settings.HA_MQTT_PUBLISH_URL
    data = {"payload" : json.dumps(result),
            "topic" : settings.HA_MQTT_ADHOC_RESULT_TOPIC,
            "retain" : settings.HA_MQTT_ADHOC_RESULT_RETAIN}
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json',
                'Authorization': 'Bearer ' + settings.HA_TOKEN}

    response = requests.post(url, data=data_json, headers=headers)
    logging.debug(pformat(response))

def adhocBackupFiles(fromPatterns, backupDirID, user_agent):
    logging.debug("Adhoc backup fromPatterns: " + str(fromPatterns))
    logging.debug("Adhoc backup backupDirID: " + backupDirID)
    logging.debug("Adhoc backup user_agent: " + user_agent)

    backupTimestamp = datetime.datetime.now().isoformat()
    drive_service = getDriveService(user_agent)

    copyCount = 0
    newCount = 0
    replacedCount = 0

    filesToCopy = []
    for fromPattern in fromPatterns:
        globResult = glob.glob(fromPattern)
        logging.debug("glob of " + fromPattern + " returned " + str(globResult))
        filesToCopy.extend(globResult)

    logging.debug("Files to copy: " + str(filesToCopy))

    for file in filesToCopy:

        file_size = os.path.getsize(file)
        if file_size == 0:
            raise Exception("The file, " + file + " is empty. This application cannot copy empty (size = 0) files to Google Drive.")
    
        matchesFound = deleteIfThere(file, backupDirID, drive_service)
        if matchesFound == 0:
            newCount += 1
        else:
            replacedCount += matchesFound
        shortFileName = ntpath.basename(file)
        MIMETYPE = mimetypes.MimeTypes().guess_type(shortFileName, False)[0]
        TITLE = shortFileName
        DESCRIPTION = 'Backup from hassio of ' + file
        backupFile(file, backupDirID, drive_service, MIMETYPE, TITLE, DESCRIPTION)
        copyCount += 1

    result = {'adhocBackupTimestamp': backupTimestamp,
                'fromPatterns': fromPatterns,
                'backupDirID': backupDirID,
                'copyCount': copyCount,
                'newCount': newCount,
                'replacedCount': replacedCount}
    return result

def backupFiles(fromPattern, backupDirID, user_agent):

    logging.debug("backup fromPattern: " + fromPattern)
    logging.debug("backup backupDirID: " + backupDirID)
    logging.debug("backup user_agent: " + user_agent)

    backupTimestamp = datetime.datetime.now().isoformat()
    drive_service = getDriveService(user_agent)

    fileCount = 0
    alreadyCount = 0
    backedUpCount = 0
    for file in glob.glob(fromPattern):
        fileCount += 1

        file_size = os.path.getsize(file)
        if file_size == 0:
            raise Exception("The file, " + file + " is empty. This application cannot copy empty (size = 0) files to Google Drive.")
    
        if alreadyBackedUp(file, backupDirID, drive_service):
            alreadyCount += 1
        else:
            # Metadata about the file.
            # Only supported file type right now is tar file.
            MIMETYPE = 'application/tar'
            TITLE = 'Hassio Snapshot'
            DESCRIPTION = 'Hassio Snapshot backup copy'
            backupFile(file, backupDirID, drive_service, MIMETYPE, TITLE, DESCRIPTION)
            backedUpCount += 1
    result = {'backupTimestamp': backupTimestamp,
                'fromPattern': fromPattern,
                'backupDirID': backupDirID,
                'fileCount': fileCount,
                'alreadyCount': alreadyCount,
                'backedUpCount': backedUpCount}
    return result

def purgeOldFiles(fromPattern, preserve):

    logging.info("Beginning purge process...")
    sourceFiles = sorted(glob.glob(fromPattern), key=os.path.getmtime)
    numSourceFiles = len(sourceFiles)
    deletedCount = 0
    if numSourceFiles > preserve:
        numToDelete = numSourceFiles - preserve
        filesToDelete = sourceFiles[:numToDelete]
        for file in filesToDelete:
            os.remove(file)
            deletedCount += 1
            logging.info("Deleted " + os.path.basename(file))
    else:
        logging.info("Nothing to purge")
    return deletedCount

def purgeOldGoogleFiles(backupDirID, preserve, user_agent):

    logging.info("Beginning purge Google Drive process...")

    drive_service = getDriveService(user_agent)

    # Search for all files in Google Drive Directory
    results = drive_service.files().list(
        q="'" + backupDirID + "' in parents and trashed = false",
        spaces='drive',
        orderBy='modifiedTime',
        fields="files(id, name)").execute()
    items = results.get('files', [])

    numSourceFiles = len(items)
    deletedCount = 0
    if numSourceFiles > preserve:
        numToDelete = numSourceFiles - preserve
        filesToDelete = items[:numToDelete]
        for file in filesToDelete:
            drive_service.files().delete(fileId=file.get('id')).execute()
            deletedCount += 1
            logging.info("Deleted " + file.get('name') + " : " + file.get('id'))
    else:
        logging.info("Nothing to purge from Google Drive")
    return deletedCount