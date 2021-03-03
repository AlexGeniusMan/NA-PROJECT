from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.ModelSerializer):
    # hall = SpecialHallSerializer(read_only=True)

    class Meta:
        depth = 2
        model = Message
        fields = '__all__'
