from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Stats, PeerkadaAccount, Notification
from peerkada.utilities.common_errors import *
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from ..serializer.get_form_stats_serializers import DisplayFormStatsSerializer
from django.forms.models import fields_for_model
from django.db import models

class GetStatsView(APIView):
    def get_stats(self, requesting_user):
        try:
            stats = Stats.objects.filter(created_by=requesting_user.id)
            return stats
        except Stats.DoesNotExist:
            data = {}
            message = 'Oops'
            errors = {}
            status = not_Found
            return Response({"message": message, "data": data, "status": status, "errors": errors})

    def calculate_total_score(self, stat):
        total_score = 0
        for field in stat._meta.get_fields():
            if (
                field.name not in ['created_by', 'id']
                and not field.is_relation
                and isinstance(field, models.IntegerField)
            ):
                total_score += int(getattr(stat, field.name, 0))

        setattr(stat, 'total_score', total_score)

    def check_mental_wellbeing(self, stat):
        # Calculate or retrieve total score
        self.calculate_total_score(stat)

        # Define your mental well-being criteria
        if 60 <= stat.total_score <= 70:
            message = "You are in the optimum state of mental wellbeing! Keep it up!"
        elif 45 <= stat.total_score <= 55:
            message = "You are in a good state of mental wellbeing!"
        elif 14 <= stat.total_score <= 44:
            message = "You are showing signs of being mentally unwell. Please take a quick rest and meditate."
        elif 10 <= stat.total_score <=13:
            message = "You are showing signs of being mentally unwell. Please take a quick rest and meditate."
            return

        Notification.objects.create(id = generate_uuid(), user=stat.created_by, message=message)

        # Retrieve user's notifications
        user_notifications = Notification.objects.filter(user=stat.created_by).order_by('created_at')

        # Delete the oldest notification if there are more than 10
        if user_notifications.count() > 10:
            oldest_notification = user_notifications.first()
            oldest_notification.delete()

    def get(self, request):
        requesting_user = request.user
        stats = self.get_stats(requesting_user)

        # Iterate over stats and check mental well-being for each
        for stat in stats:
            self.check_mental_wellbeing(stat)

        serializer = DisplayFormStatsSerializer(stats, many=True)
        data = serializer.data
        status = ok
        message = "Results"
        errors = {}

        return Response({"message": message, "data": data, "status": status, "errors": errors})
