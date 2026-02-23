from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return value

    class Meta:
        model = Game
        fields = "__all__"
