from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from movies.models import Movie, Session, Ticket
from movies.permissions import IsReservedByUser
from movies.serializers import MovieSerializer, SessionSerializer, TicketSerializer


class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieSessionList(generics.ListAPIView):
    serializer_class = SessionSerializer

    def get_queryset(self):  # type: ignore
        movie_id = self.kwargs.get("movie")
        movie = get_object_or_404(Movie, pk=movie_id)
        return Session.objects.filter(movie=movie)


class SessionTicketList(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore
        session_id = self.kwargs.get("session")
        session = get_object_or_404(Session, pk=session_id)
        return Ticket.objects.filter(session=session)


class TicketReserve(generics.GenericAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ticket = self.get_object()
        reserved, current_status = ticket.reserve(request.user)

        if not reserved:
            return Response(
                {
                    "detail": "Ticket can only be reserved when it is available.",
                    "status": current_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketPurchase(generics.GenericAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsReservedByUser]

    def post(self, request, pk):
        ticket = self.get_object()
        ticket.purchase()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)
