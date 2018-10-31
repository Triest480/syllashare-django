from django.http import HttpResponseRedirect
from django.shortcuts import render

from user_data.models import User, School, Class, SyllabusEvent
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
    body_in = json.loads(request.body.decode('utf-8'))
    
    if 'username' in body_in:
        if has_profanity(body_in['username']):
            response = HttpResponse(json.dumps({'msg': 'Username Contains Profanity'}), content_type='application/json')
            response.status_code = 400
            return response
        user.username = body_in['username']
        
    if 'firstName' in body_in:
        if has_profanity(body_in['firstName']):
            response = HttpResponse(json.dumps({'msg': 'First Name Contains Profanity'}), content_type='application/json')
            response.status_code = 400
            return response
        user.first_name = body_in['firstName']
        
    if 'lastName' in body_in:
        if has_profanity(body_in['lastName']):
            response = HttpResponse(json.dumps({'msg': 'Last Name Contains Profanity'}), content_type='application/json')
            response.status_code = 400
            return response
        user.last_name = body_in['lastName']
    
    if 'school' in body_in:
        schools = School.objects.filter(name=body_in['school'])
        if len(schools) != 1:
            response = HttpResponse(json.dumps({'msg': 'School Not Found'}), content_type='application/json')
            response.status_code = 404
            return response
        user.school = schools[0]
    try:
        user.save()
    except:
        response = HttpResponse(json.dumps({'msg': 'Username Already Exists'}), content_type='application/json')
        response.status_code = 400
        return response
    return HttpResponse(status=200)


@csrf_exempt
def get_user(request):
    user = verify_token(request)
    if not user:
        return HttpResponse(status=403)
    user_id = request.GET.get('id', '')
    if user_id:
        users = User.objects.filter(id=user_id)
        if len(users) != 1:
            response = HttpResponse(json.dumps({'msg': 'User Not Found'}), content_type='application/json')
            response.status_code = 404
            return response
        user = users[0]
    service_tokens = ServiceToken.objects.filter(user=user)
    providers = []
    for service_token in service_tokens:
        providers.append(service_token.provider)
    school_dict = {}
    if user.school:
        school_dict = {
            'name': user.school.name,
            'imgKey': user.school.pic_key
        }
    return JsonResponse(
        {
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'picKey': user.pic_key,
            'school': school_dict,
            'providers': providers
        }
    )


@csrf_exempt
def get_schools(request):
    schools = School.objects.all()
    result = []
    for school in schools:
        result.append({'name': school.name, 'picKey': school.pic_key})
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
                if teacher:
                    # pack teacher info into json
                    pass
                event_list = SyllabusEvent.objects.filter(from_class=class_obj)
                for events in event_list:
                    # pack into json
                    pass

        except ValueError:
            return HttpResponse(status=403)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
