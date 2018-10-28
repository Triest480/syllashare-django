from django.shortcuts import render
from query.models import Profile
from django.http import JsonResponse, HttpResponse
import difflib


def search_users(request):
    queryid = str(request.GET.get('query'))
    queryid = queryid.replace('"', '')
    users = []
    p = Profile.objects.all()

    for i in p:
        if queryid.lower() in str(i.first_name):
            users.append(
                {
                    "id": i.id,
                    "firstname": i.first_name,
                    "lastname": i.last_name,
                    "username": i.username,
                    "profilePicUrl": i.profilePicUrl
                }
            )
        elif queryid.lower() in str(i.last_name):
            users.append({
                "id": i.id,
                "firstname": i.first_name,
                "lastname": i.last_name,
                "username": i.username,
                "profilePicUrl": i.profilePicUrl
            })
        elif queryid.lower() in str(i.username):
            users.append({
                "id": i.id,
                "firstname": i.first_name,
                "lastname": i.last_name,
                "username": i.username,
                "profilePicUrl": i.profilePicUrl
            })

    return JsonResponse(sorted(users,
                               key=lambda x: difflib.SequenceMatcher(None,
                                                                     x['firstname'] + x['lastname'] + x['username'],
                                                                     queryid).ratio()),
                        safe=False)
