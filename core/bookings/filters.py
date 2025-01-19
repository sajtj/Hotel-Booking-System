from django_filters import FilterSet
from .models import Hotel, Room

class HotelFilter(FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'location': ['exact'],
        }

class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'capacity': ['gte', 'lte'],
        }