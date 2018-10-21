import time

from django.http import HttpResponse
from syllatokens.models import SyllaShareToken


def verify_token(request):
    try:
        user_token = request.META['HTTP_AUTHORIZATION']
        print('User Syllashare Token:', user_token)
        entries = SyllaShareToken.objects.filter(syllashare_token=user_token)
        print('Entries:', entries)
        if len(entries) == 1:
            try:
                exp_date = entries[0].expiration_date.timestamp()
                if exp_date > time.time():
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=403)
            except NameError:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=403)

    except KeyError:
        return HttpResponse(status=403)
