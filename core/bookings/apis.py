from core.common.pagination import CustomPagination
from core.common.mixins import ApiAuthMixin

from rest_framework.views import APIView
from rest_framework import serializers

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Hotel, Room, Booking
from .filters import HotelFilter, RoomFilter





class HotelApi(ApiAuthMixin, APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter
    pagination_class = CustomPagination

    class HotelOutputSerializer(serializers.ModelSerializer):
        available_rooms = serializers.SerializerMethodField()

        class Meta:
            model = Hotel
            fields = ["id", "name", "location", "available_rooms"]

        def get_available_rooms(self, obj):
            return obj.rooms.filter(bookings__isnull=True).count()


    @extend_schema(responses=HotelOutputSerializer)
    def get(self, request):
        hotels = Hotel.objects.prefetch_related("rooms").all()
        paginator = self.pagination_class()
        paginated_hotels = paginator.paginate_queryset(hotels, request)
        serializer = self.HotelOutputSerializer(paginated_hotels, many=True)
        return paginator.get_paginated_response(serializer.data)




class HotelDetailApi(ApiAuthMixin, APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter
    pagination_class = CustomPagination
    
    class HotelDetailOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = "__all__"

    
    @extend_schema(responses=HotelDetailOutputSerializer)
    def get(self, request, pk):
        rooms = Room.objects.filter(hotel=pk, bookings__isnull=True)
        paginator = self.pagination_class()
        paginated_rooms = paginator.paginate_queryset(rooms, request)
        serializer = self.HotelDetailOutputSerializer(paginated_rooms, many=True)
        return paginator.get_paginated_response(serializer.data)