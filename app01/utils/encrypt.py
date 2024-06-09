from django.conf import settings
import hashlib


def md5(data_string):
    # a = 'django-insecure-mfc^g%cl0x25noznzs#(9a1fbyj=*&kjid@6(x0ugw0(o1%vo8'
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    # obj = hashlib.md5(a.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
