from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

import logging
import traceback

from gbcommon import getOptions, backupFile, requestAuthorization, fetchAndSaveTokens, backupFiles, purgeOldFiles, purgeOldGoogleFiles, publishResult

def index(request):
    return render(request, 'gb/index.html')

def getAuth(request):

    authorization_url, state = requestAuthorization()

    # Save the value returned for state
    request.session['state'] = state

    return HttpResponseRedirect(authorization_url)

def authConfirmed(request):

    saved_state = request.session['state']
    authorizationCode = request.POST.get('authorizationCode')

    fetchAndSaveTokens(saved_state, request.build_absolute_uri(reverse('gb:authConfirmed')), request.build_absolute_uri(), authorizationCode)

    return render(request, 'gb/authConfirmed.html')

def doBackup(request):

    options = getOptions()
    fromPattern = options["fromPattern"]
    backupDirID = options["backupDirID"]
    doPurge = options["purge"]["enabled"]
    preserve = options["purge"]["preserve"]
    doGooglePurge = options["purge_google"]["enabled"]
    preserveInGoogle = options["purge_google"]["preserve"]

    backupResult = {}
    status = 200
    try:
        backupResult = backupFiles(fromPattern, backupDirID, request.build_absolute_uri('/'))
        if doPurge:
            deletedCount = purgeOldFiles(fromPattern, preserve)
            backupResult['deletedCount'] = deletedCount
        if doGooglePurge:
            deletedFromGoogleCount = purgeOldGoogleFiles(backupDirID, preserveInGoogle, request.build_absolute_uri('/'))
            backupResult['deletedFromGoogle'] = deletedFromGoogleCount
    except Exception as e:
        logging.error(traceback.format_exc())
        backupResult = {'errorMessage': str(e)}
        status = 500

    logging.info("googlebackup result: " + str(backupResult)) 
    publishResult(backupResult)

    return JsonResponse(backupResult, status=status)