from rest_framework import serializers
from alarms.models import Alarm

class AlarmSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.get_d_day_display()
        return name
    class Meta:
        model = Alarm
        fields = ['d_day', 'name']