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
import os
import re
import datetime
import ntpath
import boto3
import botocore
from django.conf import settings
import difflib

#Unused
@csrf_exempt
def sup(request):
    return HttpResponse('Sup')

#Used
@csrf_exempt
def ping(request):
    return HttpResponse(status=200)


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
        if body_in["school"] is not None:
            schools = School.objects.filter(name=body_in["school"]["name"])
            if len(schools) != 1:
                response = HttpResponse(json.dumps({'msg': 'School Not Found'}), content_type='application/json')
                response.status_code = 404
                return response
            user.school = schools[0]
        else:
            user.school = None
    try:
        user.save()
    except:
        response = HttpResponse(json.dumps({'msg': 'Username Already Exists'}), content_type='application/json')
        response.status_code = 400
        return response
    return HttpResponse(status=200)


#Used
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
    school_dict = None
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

#Unused
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

#Unused
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

#Used
@csrf_exempt
def get_schools(request):
    schools = School.objects.all()
    result = []
    for school in schools:
        result.append({'name': school.name, 'picKey': school.pic_key})
    return JsonResponse(result, safe=False)


#Unused
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

#Unused
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
def add_class(request):
    pass

#Used
@csrf_exempt
def class_scan(request):
    if request.method == 'POST':
        post_json = json.loads(request.body)

        s3_obj_key = post_json.get('objKey')
        BUCKET_NAME = 'syllasharedata'
    
        s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        )
        #This will break on async calls
        print("Downloading from s3")
        try:
            s3.Bucket(BUCKET_NAME).download_file(s3_obj_key, '/tmp/temp_pdf.pdf')
        except Exception as e:
            print("S3 download fail: ", e)
            return JsonResponse({}, status=404)
            
        print("S3 downloaded")
        
        json_response = read_file('/tmp/temp_pdf.pdf')
        try:
            os.remove('/tmp/temp_pdf.pdf')
            os.remove('/tmp/temp_pdf.txt')
        except FileNotFoundError:
            pass
        return JsonResponse(json_response)
    else:
        return JsonResponse({}, status=404)


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def read_file(file_path):
    print("In Read file")
    file_name = path_leaf(file_path)
    print("FILE NAME: ", file_name)
    path = os.path.dirname(file_path)
    print('File:', file_path)

    test_path = os.path.join(path, 'test_text_files')
    if not os.path.isdir(test_path):
        os.mkdir(test_path)

    text_file_path = os.path.join(test_path, file_name).replace('.pdf', '.txt')

    cmd = "pdftotext -layout %s %s" % (file_path, text_file_path)
    os.system(cmd)

    with open(text_file_path) as f:
        result = f.read()

    if result:

        first_name, last_name = find_professor(result)
        print('Professor:', first_name, last_name)

        class_number, class_title = find_class(result)
        print('Class Number:', class_number)
        print('Class Title:', class_title)

        print('Date Objects:')
        date_lists = find_dates(result)
        for date_obj in date_lists:
            print('Date:', date_obj['date'])
            print('Event Type:', date_obj['event_type'])
            print('Event Title:', date_obj['event_title'])
            print()

        json_response = {
            'class_number': class_number,
            'class_title': class_title,
            'teacher': first_name + ' ' + last_name,
            'events': date_lists
        }
        return json_response

    else:
        return {}


def find_professor(result_string):
    for line in result_string.split('\n'):
        is_instructor_line = False
        if line:
            lower_line = line.lower()
            lower_line = lower_line.replace(':', '')
            lower_line = lower_line.replace('phd', '')
            lower_line = lower_line.replace('ph.d', '')
            if 'instructor' in lower_line:
                lower_line = lower_line.replace('instructor', '')
                is_instructor_line = True
            if 'professor' in lower_line:
                lower_line = lower_line.replace('professor', '')
                is_instructor_line = True
            if 'prof.' in lower_line:
                first_prof_index = lower_line.find('prof.')
                second_prof_index = lower_line.find('prof.', first_prof_index + 5)
                if second_prof_index != -1:
                    lower_line = lower_line[first_prof_index:second_prof_index]
                lower_line = lower_line.replace('prof.', '')
                is_instructor_line = True
            if 'dr.' in lower_line:
                lower_line = lower_line.replace('dr.', '')
                is_instructor_line = True

            if is_instructor_line:
                name = lower_line.title().strip()
                if ',' in name:
                    if len(name.split()) == 1:
                        last_name = name.replace(',', '').strip()
                        first_name = ''
                    else:
                        last_name = name.replace(',', '').split()[0]
                        first_name = name.split()[1]
                else:
                    if len(name.split()) == 1:
                        last_name = name
                        first_name = ''
                    else:
                        last_name = name.split()[-1]
                        first_name = name.split()[0]
                return first_name, last_name
    return 'DNF', 'DNF'


def find_class(result_string):
    regex = "[A-z]{1,5} ?[0-9]{1,4}"

    for line in result_string.split('\n'):
        match = re.search(regex, line)
        if match and 'fall' not in match.group(0).lower():
            class_number_token = match.group(0)
            class_title = line.replace(class_number_token, '').strip()
            return class_number_token.replace(' ', ''), class_title
    return 'Could Not Find Class Number', 'Could Not Find Class Title'


def find_dates(result_string):
    date_events = []
    regex = "(\d\d/\d\d)|(\d/\d\d)|(\d\d/\d)"
    for line in result_string.split('\n'):
        if line:
            match = re.search(regex, line)
            if match:
                date = match.group(0)
                month, day = date.split('/')
                month = int(month)
                day = int(day)
                if 1 <= month <= 12 and 1 <= day <= 31:
                    if month < 10:
                        month_str = '0' + str(month)
                    else:
                        month_str = str(month)

                    if day < 10:
                        day_str = '0' + str(day)
                    else:
                        day_str = str(day)

                    date_line_index = line.find(date)
                    event_title = line[date_line_index + len(date):].strip()
                    event_type = get_event_type(event_title)
                    date_events.append({
                        'date': month_str + '/' + day_str + '/' + str(datetime.datetime.now().year),
                        'event_title': event_title,
                        'event_type': event_type,
                    })

    return date_events


def get_event_type(activity):
    lower_activity = activity.lower()
    if 'homework' in lower_activity:
        return 'Homework'
    elif ' due' in lower_activity:
        return 'Assignment'
    elif 'midterm' in lower_activity:
        return 'Midterm'
    elif 'final' in lower_activity:
        return 'Final'
    else:
        return 'Lecture'

#Used
@csrf_exempt
def search_users(request):
    print("Running searchUsers")
    queryid = str(request.GET.get('query'))
    queryid = queryid.replace('"', '')
    users = []
    p = User.objects.all()
    
    for i in p:
        print("Loop in searchUsers")
        if queryid.lower() in str(i.username):
            users.append({
                'id': i.id,
                'firstname': i.first_name,
                'lastname': i.last_name,
                'username': i.username,
                'email': i.email,
                'pickey': i.pic_key
            })
        elif queryid.lower() in str(i.first_name):
          users.append({
                'id': i.id,
                'firstname': i.first_name,
                'lastname': i.last_name,
                'username': i.username,
                'email': i.email,
                'pickey': i.pic_key
            })
        elif queryid.lower() in str(i.last_name):
            users.append({
                'id': i.id,
                'firstname': i.first_name,
                'lastname': i.last_name,
                'username': i.username,
                'email': i.email,
                'pickey': i.pic_key
            })
    print("SearchUsers responding")
    if not users:
        return HttpResponse(status=404)
    else:
        #Doesn't make sense to sort
        return JsonResponse(sorted(users,
                                     key=lambda x: difflib.SequenceMatcher(None,
                                     x['username'],
                                     queryid).ratio()),
                                     safe=False)