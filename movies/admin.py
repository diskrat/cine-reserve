from django.contrib import admin

# Register your models here.
from .models import Movie, Session


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_date", "created_at", "updated_at"]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["movie_id", "time", "created_at", "updated_at"]
