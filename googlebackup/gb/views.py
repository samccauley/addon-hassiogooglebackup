from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

import pprint
import traceback

from gbcommon import getOptions, backupFile, requestAuthorization, fetchAndSaveTokens, backupFiles

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

    backupResult = {}
    status = 200
    try:
        backupResult = backupFiles(fromPattern, backupDirID, request.build_absolute_uri('/'))
    except Exception as e:
        print(traceback.format_exc())
        backupResult = {'errorMessage': str(e)}
        status = 500

    return JsonResponse(backupResult, status=status)