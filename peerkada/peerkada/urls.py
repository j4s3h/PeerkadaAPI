"""
URL configuration for peerkada project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.features.versions.v1p0.register_account.views.register_account_views import RegisterAccountViews, RegisterAccountCounselorViews
from core.features.versions.v1p0.login.views.login_views import LoginView
from core.features.versions.v1p0.create_forms_stats.views.create_form_stats import CreateFormStatsViews
from core.features.versions.v1p0.get_stats.views.get_stats_views import GetStatsView
from core.features.versions.v1p0.get_stats_with_average.views.display_stats_with_average import CalculateAveragesView
from core.features.versions.v1p0.get_notifications.views.get_notification_views import GetNotificationView
from core.features.versions.v1p0.read_notification.views.read_notifications_views import MarkNotificationAsReadView
from core.features.versions.v1p0.create_new_chat_or_display_chat.views.conversation_views import ConversationViews ,ConversationMessageViews, ReadConversationViews
from core.features.versions.v1p0.create_appointment.views.create_appointment_views import CreateAppointmentView
from core.features.versions.v1p0.display_appointment.views.display_appointment_views import DisplayAppointmentViews
from core.features.versions.v1p0.edit_appointment.views.edit_appointment_views import EditAppointmentViews
from core.features.versions.v1p0.delete_appointment.views.delete_appointment_views import DeleteAppointmentViews
from core.features.versions.v1p0.create_emotions_sharing.views.create_emotions_views import CreateEmotionViews
from core.features.versions.v1p0.display_emotion.views.display_emotion_views import DisplayEmotionViews, DisplayEmotionIndivViews, DisplayEmotionByUserViews, DisplayEmotionViewsWithoutPagination
from core.features.versions.v1p0.edit_last_form_stats.views.edit_last_form_views import EditFormStatsViews
from core.features.versions.v1p0.display_counselors.views.display_counselors_views import DisplayPeerkadaCounselorViews
from core.features.versions.v1p0.create_conversation_chat_with_counselor.views.conversation_with_counselor_views import CreateCounselorMessagesViews, UserReplyToMessagesViews, ReadCounselorMesssagesViews
from core.features.versions.v1p0.user_list.views.list_of_register_accounts_views import ListOfRegisteredAccounts
from core.features.versions.v1p0.display_appointment_notifications.views.display_appointment_notifications_views import DisplayAppointmentNotificationView, MarkAppointmentNotificationReadView
from core.features.versions.v1p0.approve_appointment.views.approve_appointment_views import ApproveAppointmentViews
from core.features.versions.v1p0.display_my_user_profile.views.display_user_profile_views import DisplayMyProfileViews
from core.features.versions.v1p0.edit_profile.views.edit_profile_views import EditProfileViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1p0/register/account/', RegisterAccountViews.as_view(), name = 'register_account'),
    path ('v1p0/register/account/counselor/', RegisterAccountCounselorViews.as_view(), name = 'register_account_counselor' ),
    path ('v1p0/regular/login/', LoginView.as_view(), name = 'login_view'),
    path ('v1p0/create/stats/', CreateFormStatsViews.as_view() ,name = 'create_form'),
    path ('v1p0/display/stats/', GetStatsView.as_view(), name = 'display_profile_stats'),
    path ('v1p0/calculate/stats/', CalculateAveragesView.as_view(), name ='calculate_profile_average'),
    path ('v1p0/user/notification/',GetNotificationView.as_view(), name = 'get_notification'),
    path ('v1p0/user/notification/read/<notification_id>', MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),
    path ('v1p0/conversations/', ConversationViews.as_view(), name ='conversation'),
    path ('v1p0/conversations/send/messages/', ConversationMessageViews.as_view(), name = 'send_message'),
    path('v1p0/conversations/<str:conversation_id>/', ReadConversationViews.as_view(), name='read_conversation'),
    path('v1p0/create/appointment/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('v1p0/display/appointment/', DisplayAppointmentViews.as_view(), name='display_appointment_by_the_one_who_created_by'),
    path('v1p0/edit/appointment/<pk>/',EditAppointmentViews.as_view(),name = 'edit_appointment'),
    path('v1p0/delete/appointment/<pk>/',DeleteAppointmentViews.as_view(),name = 'delete_appointment'),
    path('v1p0/create/emotion/', CreateEmotionViews.as_view(), name = 'create_emotion_views'),
    path('v1p0/display/emotions/', DisplayEmotionViews.as_view(), name = 'display_emotion_views'),
    path('v1p0/display/emotion/', DisplayEmotionViewsWithoutPagination.as_view(), name = 'display_emotions_without_pagination'),
    path('v1p0/display/emotion/<pk>/', DisplayEmotionIndivViews.as_view(), name = 'display_emotion_individual_views'),
    path ('v1p0/display/emotion/user/<str:user_id>/',DisplayEmotionByUserViews.as_view(), name = 'display_emotion_by_user'),
    path('v1p0/edit/form/', EditFormStatsViews.as_view(), name = 'edit_form_stats_view'),
    path('v1p0/display/counselor/', DisplayPeerkadaCounselorViews.as_view(), name = 'display_counselor'),
    path('v1p0/chat/', CreateCounselorMessagesViews.as_view(), name = 'create_counselor_messsages'),
    path('v1p0/chat/<str:conversation_id>/', UserReplyToMessagesViews.as_view(),name ='view_conversation'),
    path('v1p0/display/chat/',ReadCounselorMesssagesViews.as_view(), name = 'read_counselor_chat'),
    path('v1p0/display/registered_accounts/', ListOfRegisteredAccounts.as_view(),  name = 'display_registered_accounts'),
    path('v1p0/user/appointment_notification/', DisplayAppointmentNotificationView.as_view(), name = 'display_appointment_notification'),
    path('v1p0/user/appointment_notification/read/<notification_id>/', MarkAppointmentNotificationReadView.as_view(), name = 'read_appointment_notification'),
    path('v1p0/approve/appointment/<appointment_id>/', ApproveAppointmentViews.as_view(), name = 'approve_appointment'),
    path('v1p0/profile/', DisplayMyProfileViews.as_view(), name = 'display_profile'),
    path('v1p0/profile/edit/', EditProfileViews.as_view(), name = 'edit_profile_views')
]

         

