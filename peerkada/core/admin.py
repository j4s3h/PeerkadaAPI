from django.contrib import admin
from core.models import PeerkadaAccount, Stats, Notification, Conversation, ConversationMessages, Appointment, ConversationWithCounselors, CounselorMessages
# Register your models here.
admin.site.register(PeerkadaAccount)
admin.site.register(Stats)
admin.site.register(Notification)
admin.site.register(Conversation)
admin.site.register(ConversationMessages)
admin.site.register(Appointment)
admin.site.register(ConversationWithCounselors)
admin.site.register(CounselorMessages)