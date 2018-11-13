from django.http import HttpResponseRedirect
from django.shortcuts import render

from user_data.models import User, School, Class, SyllabusEvent
from syllatokens.models import ServiceToken
from syllatokens.utils import verify_token
from user_data.utils import has_profanity
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import traceback
import itertools
import difflib


@csrf_exempt
def sup(request):
    return HttpResponse('Sup')


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
    
    if "school" in body_in:
        schools = School.objects.filter(name=body_in["school"]["name"])
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
            'picKey': user.school.pic_key
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
def follow_class(request):
    if request.method == 'POST':

        user = verify_token(request)
        if not user:
            return HttpResponse(status=403)

        post_json = json.loads(request.body)
        class_pk = post_json.get('classID')
        if class_pk.startswith('"') and class_pk.endswith('"'):
            class_pk = class_pk[1:-1]
        try:
            class_pk_int = int(class_pk)
        except TypeError:
            return HttpResponse(status=400)
        try:
            class_obj = Class.objects.get(pk=class_pk_int)
            user.classes.remove(class_obj)
            return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)


@csrf_exempt
def unfollow_class(request):
    if request.method == 'POST':

        user = verify_token(request)
        if not user:
            user = User.objects.get(pk=0)
            # return HttpResponse(status=403)

        post_json = json.loads(request.body)
        class_pk = post_json.get('classID')
        if class_pk.startswith('"') and class_pk.endswith('"'):
            class_pk = class_pk[1:-1]
        try:
            class_pk_int = int(class_pk)
        except TypeError:
            return HttpResponse(status=400)
        try:
            class_obj = Class.objects.get(pk=class_pk_int)
            user.classes.remove(class_obj)
            return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

@csrf_exempt
def get_schools(request):
    schools = School.objects.all()
    result = []
    for school in schools:
        result.append({'name': school.name, 'picKey': school.pic_key})
    return JsonResponse(result, safe=False)


@csrf_exempt
def search_classes(request):
    query_str = request.GET.get('query', '')
    if query_str.startswith('"') and query_str.endswith('"'):
        query_str = query_str[1:-1]
    class_number_results = Class.objects.filter(class_number__contains=query_str)
    class_description_results = Class.objects.filter(class_description__contains=query_str)
    classes = list(itertools.chain(class_description_results, class_number_results))

    class_json_list = []
    for class_obj in classes:
        class_json = {
            'name': class_obj.class_description,
            'classNumber': class_obj.class_number,
            'subject': class_obj.department.department_name
        }
        class_json_list.append(class_json)
    return JsonResponse(class_json_list, safe=False)


@csrf_exempt
def get_class_schedule(request):
    class_id = request.GET.get('classID', '')
    if class_id.startswith('"') and class_id.endswith('"'):
        class_id = class_id[1:-1]  # strip off first " and last "
    if class_id:
        try:
            class_id_num = int(class_id)
            if Class.objects.filter(pk=class_id_num).exists():
                class_obj = Class.objects.get(pk=class_id_num)
                teacher = class_obj.teacher
                teacher_json = {}
                if teacher:
                    # pack teacher info into json
                    teacher_json = {
                        'name': '{} {}'.format(teacher.first_name, teacher.last_name),
                        'rating': teacher.rating,
                        'department': teacher.department.department_name,
                        'school': teacher.school.name,
                    }
                events = SyllabusEvent.objects.filter(from_class=class_obj)
                event_json_list = []
                for event in events:
                    event_json = {
                        'id': event.pk,
                        'name': event.event_name,
                        'eventType': event.event_type.event_type,
                        'date': event.date,
                    }
                    event_json_list.append(event_json)
                return JsonResponse(
                    {
                        'teacher': teacher_json,
                        'events': event_json_list
                    })
            else:
                return JsonResponse({}, status=404)
        except ValueError:
            traceback.print_exc()
            return JsonResponse({}, status=403)
    else:
        return JsonResponse({}, status=404)


@csrf_exempt
def search_users(request):
    query_str = request.GET.get('query', '')
    if query_str.startswith('"') and query_str.endswith('"'):
        query_str = query_str[1:-1]
    query_str = query_str.lower()
    if len(query_str) < 3:
        return HttpResponse(status=400)

    user_list = []
    for user in User.objects.all():
        if len(user_list) > 20:
            break
        else:
            if query_str in user.username:
                user_list.append({
                    'id': user.id,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'username': user.username,
                    'email': user.email,
                    'pickey': user.pic_key,
                })
    if len(user_list) < 20:
        for user in User.objects.all():
            if user.first_name and query_str in user.first_name or user.last_name and query_str in user.last_name:
                if user not in user_list:
                    user_list.append({
                        'id': user.id,
                        'firstname': user.first_name,
                        'lastname': user.last_name,
                        'username': user.username,
                        'email': user.email,
                        'picKey': user.pic_key,
                    })
    if len(user_list) > 20:
        return JsonResponse(user_list[:20], safe=False)
    else:
        return JsonResponse(user_list, safe=False)