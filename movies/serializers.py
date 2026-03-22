from django.contrib.auth.models import User
from rest_framework import serializers
from movies.models import Movie, Session, Ticket


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "release_date", "length", "pg", "director"]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["id", "movie_id", "time", "type"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "session", "status", "chair", "user"]
