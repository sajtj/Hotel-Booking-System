from django.urls import path
from .apis import HotelApi, HotelDetailApi

urlpatterns = [
    path("hotels/", HotelApi.as_view(), name="hotels"),
    path("hotels/<int:pk>/", HotelDetailApi.as_view(), name="hotel-rooms"),
]