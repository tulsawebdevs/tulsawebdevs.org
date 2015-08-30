from django.conf import settings


def webpack_debug(request):
    context_extras = {'webpack_debug': False}
    if settings.WEBPACK_DEBUG and request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
        context_extras['webpack_debug'] = True
    return context_extras
