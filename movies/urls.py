from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from movies import views

urlpatterns = [
    path("movies/", views.MovieList.as_view()),
    path("movies/<int:movie>/sessions", views.MovieSessionList.as_view()),
    path("sessions/<int:session>/tickets/", views.SessionTicketList.as_view()),
    path("tickets/<int:pk>/reserve", views.TicketReserve.as_view()),
    path("tickets/<int:pk>/purchase", views.TicketPurchase.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
