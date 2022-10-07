from rest_framework import serializers
from .models import Team, Booking, Match

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields='__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields='__all__'




class MatchSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    booking_time = BookingSerializer(read_only=True)
    class Meta:
        model = Match
        fields = '__all__'