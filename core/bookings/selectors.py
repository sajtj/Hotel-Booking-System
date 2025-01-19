from django.db.models import QuerySet
from core.users.models import BaseUser
from .models import Hotel, Room, Booking


def hotel_list() -> QuerySet[Hotel]:
    return Hotel.objects.prefetch_related("rooms").all()

def available_rooms_list(*, hotel_id:int) -> QuerySet[Room]:
    return Room.objects.filter(hotel=hotel_id, bookings__isnull=True)

def get_room(*, room_id:int) -> Room:
    return Room.objects.get(id=room_id)

def booking_list(*, user:BaseUser) -> QuerySet[Booking]:
    return Booking.objects.filter(user=user)

def room_booking_list(*, user:BaseUser, room_id:int) -> QuerySet[Booking]:
    return Booking.objects.filter(user=user, room=room_id)

def get_booking(*, user:BaseUser, booking_id:int) -> Booking:
    return Booking.objects.get(id=booking_id, user=user)