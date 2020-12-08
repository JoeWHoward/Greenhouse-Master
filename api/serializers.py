from rest_framework import serializers
from .models import TempHumRecord

class TempHumRecordSerializer(serializers.ModelSerializer):
    temp = serializers.FloatField()
    humidity = serializers.FloatField()
    #date_time_logged = serializers.DateTimeField(required=False)

    class Meta:
        model = TempHumRecord
        fields = ('temp', 'humidity')
    

    # TODO: implement some more rigorous validation/error handling here
    def to_internal_value(self, data): # Handling data validation by lazily casting the JSON string output from ESP to float
        values = super().to_internal_value(data)
        values['temp'] = float(data['temp'])
        values['humidity'] = float(data['humidity'])
        return values