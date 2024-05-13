from rest_framework import serializers

from app.models import Message


class MessageSerializers(serializers.ModelSerializer):
    user_from = serializers.CharField()
    user_to = serializers.CharField()
    message = serializers.CharField()

    class Meta:
        model = Message
        fields = '__all__'
