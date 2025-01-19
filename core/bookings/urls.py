from django.urls import path
from .apis import HotelApi, HotelDetailApi, RoomDetailApi, BookingApi, BookingDetailApi, RoomBookingApi

urlpatterns = [
    path("", BookingApi.as_view(), name="bookings"), #all bookings
    path("<int:booking_id>/", BookingDetailApi.as_view(), name="booking-detail"),
    path("rooms/<int:room_id>/", RoomBookingApi.as_view(), name="booking-rooms"),
    

    path("hotels/", HotelApi.as_view(), name="hotels"),
    path("hotels/<int:hotel_id>/", HotelDetailApi.as_view(), name="hotel-rooms"),
    path("hotels/rooms/<int:room_id>", RoomDetailApi.as_view(), name="hotel-rooms-detail"),
    
]