from django.contrib import admin

from talks.models import Talk, Speaker


admin.site.register(Talk)
admin.site.register(Speaker)
