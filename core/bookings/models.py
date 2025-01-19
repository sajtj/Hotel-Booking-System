from django.db import models
from core.common.models import BaseModel
from core.users.models import BaseUser


class Hotel(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Room(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hotel", "number"],
                name="unique_room_number_per_hotel"
            )
        ]
    
    def __str__(self):
        return f"{self.hotel}  -  {self.number}"

class Booking(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "start_time", "end_time"],
                name="unique_booking_constraint",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.room} | {self.start_time} - {self.end_time}"