from rest_framework import serializers
from core.models import PeerkadaAccount, Stats

class CreateFormStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = [ 'optimism','usefulness' ,'relaxed',
    'interest_in_others' ,
    'energy_to_spare',
    'deal_with_problems_well',
    'clearliness',
    'good_about_yourself',
    'close_to_other_people',
    'confident' ,
    'make_up_your_own_mind_about_things' ,
    'loved' ,
    'interested_in_new_things' ,
    'cheerfulness', ]


   