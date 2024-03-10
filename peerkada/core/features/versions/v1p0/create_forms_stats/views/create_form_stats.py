from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Stats, PeerkadaAccount, Notification
from django.db import models
from peerkada.utilities.common_errors import *
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from ..serializer.create_form_stats_serializers import CreateFormStatsSerializer
from django.forms.models import fields_for_model


class CreateFormStatsViews(APIView):
    permission_classes = [IsAuthenticated]

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
        elif 14 <= stat.total_score <= 42:
            message = "You are showing signs of being mentally unwell. Please take a quick rest and meditate."
            return
       
        # Retrieve user's notifications
        user_notifications = Notification.objects.filter(user=stat.created_by).order_by('created_at')
        uid =generate_uuid()
        # Create a notification for the user
        new_notification = Notification.objects.create(user=stat.created_by,id= uid, message=message)

        # Delete the oldest notification if there are more than 10
        if user_notifications.count() > 10:
            oldest_notification = user_notifications.first()
            oldest_notification.delete()


    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id

        # Check if the user has created Stats in the last 24 hours
        last_24_hours = timezone.now() - timezone.timedelta(hours=24)
        recent_stats = Stats.objects.filter(created_by=request.user, created_at__gte=last_24_hours)

        if recent_stats.exists():
            time_difference = (timezone.now() - recent_stats.first().created_at).total_seconds() / 3600
            message = f'You can only create Stats once every 24 hours. Please wait for {24 - time_difference:.2f} hours.'
            return Response({'message': message}, bad_request)

        serializer = CreateFormStatsSerializer(data=data)

        if serializer.is_valid():
            uid = generate_uuid()

            # Create Stats instance
            stats = Stats.objects.create(
                id=uid,
                created_by=request.user,
                optimism=data['optimism'],
                usefulness=data['usefulness'],
                relaxed=data['relaxed'],
                interest_in_others=data['interest_in_others'],
                energy_to_spare=data['energy_to_spare'],
                deal_with_problems_well=data['deal_with_problems_well'],
                clearliness=data['clearliness'],
                good_about_yourself=data['good_about_yourself'],
                close_to_other_people=data['close_to_other_people'],
                confident=data['confident'],
                make_up_your_own_mind_about_things=data['make_up_your_own_mind_about_things'],
                loved=data['loved'],
                interested_in_new_things=data['interested_in_new_things'],
                cheerfulness=data['cheerfulness']
            )

            # Perform mental well-being check and create notification
            self.check_mental_wellbeing(stats)

            created_by_data = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'birthday': str(request.user.birthday),
                'sex': request.user.sex,
            }

            response_data = {
                'id': uid,
                'created_by': created_by_data,
                'optimism': data['optimism'],
                'usefulness': data['usefulness'],
                'relaxed': data['relaxed'],
                'interest_in_others': data['interest_in_others'],
                'energy_to_spare': data['energy_to_spare'],
                'deal_with_problems_well': data['deal_with_problems_well'],
                'clearliness': data['clearliness'],
                'good_about_yourself': data['good_about_yourself'],
                'close_to_other_people': data['close_to_other_people'],
                'confident': data['confident'],
                'make_up_your_own_mind_about_things': data['make_up_your_own_mind_about_things'],
                'loved': data['loved'],
                'interested_in_new_things': data['interested_in_new_things'],
                'cheerfulness': data['cheerfulness'],
                'total_score': stats.total_score,
            }

            errors = {}
            status = ok
            message = 'Successfully created'

            return Response({'message': message, 'data': response_data, 'status': status, 'errors': errors})

        message = 'Oops'
        errors = serializer.errors
        status = forbidden
        return Response({'message': message, 'data': data, 'status': status, 'errors': errors})