from rest_framework import serializers
from alarms.models import Alarm

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ['d_day']