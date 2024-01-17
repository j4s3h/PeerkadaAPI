from django.contrib import admin
from core.models import PeerkadaAccount, Stats, Notification
# Register your models here.
admin.site.register(PeerkadaAccount)
admin.site.register(Stats)
admin.site.register(Notification)
