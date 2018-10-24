import time
import requests
import json
import datetime

from django.conf import settings
from django.http import HttpResponse
from syllatokens.models import ServiceTokens
from django.views.decorators.csrf import csrf_exempt
from syllatokens.utils import verify_token
from django.http import JsonResponse

@csrf_exempt
def exchange_google_code(request):
    google_client_id = settings.GOOGLE_CLIENT_ID
    google_client_secret = settings.GOOGLE_CLIENT_SECRET
    
    user = verify_token(request)
    if (user is None):
        return HttpResponse(status=403)
        
    body_in = json.loads(request.body.decode("utf-8"))
    
    headers = {
        "content-type": "application/json" 
    }
    body_google_req = {
        "code": body_in["code"],
        "client_id": google_client_id,
        "client_secret": google_client_secret,
        "redirect_uri": "postmessage",  #I don't why but this has to be postmessage
        "grant_type": "authorization_code"
    }
    google_response = requests.post("https://www.googleapis.com/oauth2/v4/token", json=body_google_req, headers=headers)
    print("GOOGLE RESP: ", google_response.text)
    body_google_resp = json.loads(google_response.text)
    if "refresh_token" in body_google_resp:
        exp_date = datetime.datetime.utcnow() + datetime.timedelta(seconds = body_google_resp["expires_in"])
        ServiceTokens.objects.create(access_token=body_google_resp["access_token"], refresh_token=body_google_resp["refresh_token"], provider="google", expiration_date=exp_date, user_id=user.id)
    return JsonResponse({'idToken': body_google_resp["id_token"], "accessToken": body_google_resp["access_token"]})

@csrf_exempt     
def reassign_google_token(request):
    user = verify_token(request)
    if (user is None):
        return HttpResponse(status=403)
        
    body_in = json.loads(request.body.decode("utf-8"))
    access_token = body_in["accessToken"]
    print("Access token: ", access_token)
    entries = ServiceTokens.objects.filter(access_token=access_token)
    if len(entries) == 1:
        exp_date = entries[0].expiration_date.timestamp()
        if exp_date > time.time():
            entries[0].user_id = user.id
            entries[0].save()
            return HttpResponse(status=200)
    return HttpResponse(status=404)