from django.db import transaction
from core.users.models import BaseUser
from datetime import datetime
from .models import Room, Booking

@transaction.atomic
def create_booking(*, user:BaseUser, room_id:int, start_time:datetime, end_time:datetime) -> Booking:
    # Lock the room to prevent race conditions
    room = Room.objects.select_for_update().get(id=room_id)
    booking = Booking.objects.create(
        user=user, room=room, start_time=start_time, end_time=end_time
    )
    return booking

def unbooking(*, booking_id:int) -> None:
    Booking.objects.get(id=booking_id).delete()