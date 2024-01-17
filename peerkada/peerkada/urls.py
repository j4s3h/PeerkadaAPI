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
from core.features.versions.v1p0.forms_stats.views.create_form_stats import CreateFormStatsViews
from core.features.versions.v1p0.get_stats.views.get_stats_views import GetStatsView
from core.features.versions.v1p0.get_stats_with_average.views.display_stats_with_average import CalculateAveragesView
from core.features.versions.v1p0.get_notifications.views.get_notification_views import GetNotificationView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1p0/register/account/', RegisterAccountViews.as_view(), name = 'register_account'),
    path ('v1p0/register/account/counselor/', RegisterAccountCounselorViews.as_view(), name = 'register_account_counselor' ),
    path ('v1p0/regular/login/', LoginView.as_view(), name = 'login_view'),
    path ('v1p0/create/stats/', CreateFormStatsViews.as_view() ,name = 'create_form'),
    path ('v1p0/display/stats/', GetStatsView.as_view(), name = 'display_profile_stats'),
    path ('v1p0/calculate/stats/', CalculateAveragesView.as_view(), name ='calculate_profile_average'),
    path ('v1p0/user/notification/',GetNotificationView.as_view(), name = 'get_notification')
    
]
