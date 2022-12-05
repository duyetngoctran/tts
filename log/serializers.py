from rest_framework import serializers
from .models import Speak


class SpeakSerializer(serializers.ModelSerializer):

    class Meta:
        model = Speak
        fields = ('txt', 'timestamp', 'username')