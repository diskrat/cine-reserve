from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Movie(Base):
    title = models.CharField(max_length=100)
    release_date = models.DateField("Date released")
    length = models.IntegerField("length in minutes")
    pg = models.IntegerField("parental guidance")
    director = models.CharField(max_length=100)

    class Meta:  # type: ignore
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} - {self.release_date.strftime('%Y')}"


class Session(Base):
    movie = models.ForeignKey(Movie, related_name="Sessions", on_delete=models.CASCADE)
    time = models.DateTimeField("Session time")
    type = models.CharField(max_length=50)

    class Meta:  # type: ignore
        ordering = ["time"]

    def __str__(self) -> str:
        return f"{self.movie} - {self.time.strftime('%m-%d %H:%M')} - {self.type}"


class Ticket(Base):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        PURCHASED = "purchased", "Purchased"

    session = models.ForeignKey(
        Session, related_name="Tickets", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    chair = models.IntegerField()
    user = models.ForeignKey(
        User, related_name="Tickets", on_delete=models.SET_NULL, null=True
    )
    reserved_at = models.DateTimeField(null=True, blank=True)
    reservation_duration = timedelta(seconds=30)

    @property
    def is_reservation_expired(self):
        if self.status == self.Status.RESERVED and self.reserved_at:
            return timezone.now() > (self.reserved_at + self.reservation_duration)
        return False

    def get_status(self):
        if self.is_reservation_expired or not self.user:
            self.status = self.Status.AVAILABLE
        return self.status

    def reserve(self, user):
        if self.get_status() == self.Status.AVAILABLE:
            self.status = self.Status.RESERVED
            self.user = user
            self.reserved_at = timezone.now()
            self.save(update_fields=["status", "user", "reserved_at", "updated_at"])
            return True, self.status
        return False, self.status

    def purchase(self):
        self.status = self.Status.PURCHASED
        self.reserved_at = None
        self.save(update_fields=["status", "reserved_at", "updated_at"])

    def __str__(self) -> str:
        return f"seat: {self.chair} - {self.session} - {self.session.time} - {self.session.movie.title} "
