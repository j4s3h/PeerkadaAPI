from rest_framework.response import Response
from core.models import Stats
from rest_framework.views import APIView
from peerkada.utilities.constant import *
from django.utils import timezone
from datetime import timedelta


class CalculateAveragesView(APIView):
    def get(self, request):
        user_stats = Stats.objects.filter(created_by=request.user)

        if not user_stats.exists():
            return Response({'message': 'No stats found for the authenticated user.'}, status=not_Found)

        weekly_averages = self.calculate_averages(user_stats, weeks=1)
        monthly_averages = self.calculate_averages(user_stats, weeks=4)

        message = 'Success'
        data = {
            'weekly_averages': weekly_averages,
            'monthly_averages': monthly_averages,
            'overall_averages': self.calculate_overall_averages(user_stats),  # Include overall averages
        }

        errors = {}
        status = ok
        return Response({"message": message, "data": data, "status": status, "errors": errors})

    def calculate_averages(self, stats, weeks):
        time_period_ago = timezone.now() - timedelta(weeks=weeks)
        stats_last_period = stats.filter(created_at__gte=time_period_ago)

        worried_traits = ['deal_with_problems_well', 'clearliness', 'make_up_your_own_mind_about_things']
        happy_traits = ['optimism', 'usefulness', 'energy_to_spare', 'good_about_yourself', 'close_to_other_people', 'confident', 'loved', 'cheerfulness']
        angry_traits = ['deal_with_problems_well', 'clearliness']
        sad_traits = ['optimism', 'good_about_yourself']
        positive_traits = ['optimism', 'usefulness', 'relaxed', 'interest_in_others', 'energy_to_spare', 'deal_with_problems_well',
                           'clearliness', 'good_about_yourself', 'close_to_other_people', 'confident', 'make_up_your_own_mind_about_things',
                           'loved', 'interested_in_new_things', 'cheerfulness']

        def calculate_average_for_set(trait_set):
            if trait_set == sad_traits or trait_set == worried_traits or trait_set == angry_traits:
                total_values = sum(5 - getattr(stat, trait) for stat in stats_last_period for trait in trait_set)
            else:
                total_values = sum(getattr(stat, trait) for stat in stats_last_period for trait in trait_set)
            
            count = len(stats_last_period) * len(trait_set)
            return total_values / count if count > 0 else 0

        worried_average = calculate_average_for_set(worried_traits)
        happy_average = calculate_average_for_set(happy_traits)
        angry_average = calculate_average_for_set(angry_traits)
        sad_average = calculate_average_for_set(sad_traits)
        positive_average = calculate_average_for_set(positive_traits)

        return {
            'worried_average': worried_average,
            'happy_average': happy_average,
            'angry_average': angry_average,
            'sad_average': sad_average,
            'positive_average': positive_average
        }

    def calculate_overall_averages(self, stats):
        all_traits = ['optimism', 'usefulness', 'relaxed', 'interest_in_others', 'energy_to_spare',
                      'deal_with_problems_well', 'clearliness', 'good_about_yourself', 'close_to_other_people',
                      'confident', 'make_up_your_own_mind_about_things', 'loved', 'interested_in_new_things',
                      'cheerfulness']

        overall_values = [sum(getattr(stat, trait) for trait in all_traits) for stat in stats]
        overall_average = sum(overall_values) / len(stats) if len(stats) > 0 else 0

        return {'overall_average': overall_average}