from django.urls import path

from syllatokens.views import exchange_google_code, reassign_google_token
from user_data.views import get_class_schedule, modify_user, get_user, get_schools, search_classes, \
    search_users, follow_class, unfollow_class, class_scan, ping

urlpatterns = [
    path(r'exchangegoogle', exchange_google_code),
    path(r'reassigngoogle', reassign_google_token),
    path(r'modifyuser', modify_user),
    path(r'getuser', get_user),
    path(r'searchusers', search_users),
    path(r'getschools', get_schools),
    path(r'classschedule', get_class_schedule),
    path(r'searchclasses', search_classes),
    path(r'followclass', follow_class),
    path(r'unfollowclass', unfollow_class),
    path(r'classscan', class_scan),
    path(r'ping', ping),
]
