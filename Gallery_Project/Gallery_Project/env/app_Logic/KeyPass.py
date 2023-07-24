from decouple import config

class SETTINGS_KEYS:

    djky = config('DJANGO_KEY')
    urne = config('USER_NAME')
    pawd = config('PASSWORD_KEY')
    dbstt = config('DEGUB_STATE', bool)
    emht = config('EMAIL_HOSTING')
    emun = config('EMAIL_USER')
    empw = config('EMAIL_PASSWORD')
    embe = config('EMAIL_BACKEND_SMTP')
    empt = config('EMAIL_PORT')
    emtst = config('TESTERS')
