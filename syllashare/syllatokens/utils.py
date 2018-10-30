import time
from syllatokens.models import SyllaShareToken


def verify_token(request):
    try:
        user_token = request.META['HTTP_AUTHORIZATION']
        print('User Syllashare Token:', user_token)
        entries = SyllaShareToken.objects.filter(syllashare_token=user_token)
        print('Entries:', entries)
        if len(entries) == 1:
            exp_date = entries[0].expiration_date.timestamp()
            if exp_date > time.time():
                return entries[0].user
    except (KeyError, NameError) as e:
        print("KEY ERROR", e)
        return None
