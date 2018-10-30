from django.http import HttpResponseRedirect
from django.shortcuts import render

from user_data.models import User, School, Class
from syllatokens.models import ServiceToken
from syllatokens.utils import verify_token
from user_data.utils import has_profanity
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def modify_user(request):
    user = verify_token(request)
    if not user:
        return HttpResponse(status=403)
    body_in = json.loads(request.body.decode("utf-8"))
    
    if "username" in body_in:
        if has_profanity(body_in["username"]):
            response = HttpResponse(json.dumps({"msg": "Username Contains Profanity"}), content_type='application/json')
            response.status_code = 400
            return response
        user.username = body_in["username"]
        
    if "firstName" in body_in:
        if has_profanity(body_in["firstName"]):
            response = HttpResponse(json.dumps({"msg": "First Name Contains Profanity"}), content_type='application/json')
            response.status_code = 400
            return response
        user.first_name = body_in["firstName"]
        
    if "lastName" in body_in:
        if has_profanity(body_in["lastName"]):
            response = HttpResponse(json.dumps({"msg": "Last Name Contains Profanity"}), content_type='application/json')
            response.status_code = 400
            return response
        user.last_name = body_in["lastName"]
    
    if "school" in body_in:
        schools = School.objects.filter(name=body_in["school"])
        if len(schools) != 1:
            response = HttpResponse(json.dumps({"msg": "School Not Found"}), content_type='application/json')
            response.status_code = 404
            return response
        user.school = schools[0]
    try:
        user.save()
    except:
        response = HttpResponse(json.dumps({"msg": "Username Already Exists"}), content_type='application/json')
        response.status_code = 400
        return response
    return HttpResponse(status=200)


@csrf_exempt
def get_user(request):
    user = verify_token(request)
    if not user:
        return HttpResponse(status=403)
    userID = request.GET.get('id', '')
    if userID:
        users = User.objects.filter(id=userID)
        if len(users) != 1:
            response = HttpResponse(json.dumps({"msg": "User Not Found"}), content_type='application/json')
            response.status_code = 404
            return response
        user = users[0]
    serviceTokens = ServiceToken.objects.filter(user=user)
    providers = []
    for serviceToken in serviceTokens:
        providers.append(serviceToken.provider)
    schoolDict = None
    if user.school:
        schoolDict = {
            "name": user.school.name,
            "imgKey": user.school.pic_key
        }
    return JsonResponse({"username": user.username, "firstName": user.first_name, "lastName": user.last_name, "picKey": user.pic_key, "school": schoolDict, "providers": providers})


@csrf_exempt
def get_schools(request):
    schools = School.objects.all()
    result = []
    for school in schools:
        result.append({"name": school.name, "picKey": school.pic_key})
    return JsonResponse(result, safe=False)


@csrf_exempt
def get_class_schedule(request):
    class_id = request.GET.get('classID', '')
    print('Class ID:', class_id)
    if class_id:
        try:
            class_id_num = int(class_id)
            if Class.objects.filter(pk=class_id_num).exists():
                class_obj = Class.objects.get(pk=class_id_num)
                teacher = class_obj.teacher

        except ValueError:
            return HttpResponse(status=403)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
