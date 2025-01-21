from core.common.pagination import CustomPagination
from core.common.mixins import ApiAuthMixin

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers

from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema

from datetime import timedelta

from .models import Hotel, Room, Booking
from .filters import HotelFilter, RoomFilter
from .services import create_booking, unbooking
from .selectors import hotel_list, get_room, room_list, booking_list, room_booking_list, get_booking



class HotelApi(ApiAuthMixin, APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter
    pagination_class = CustomPagination

    class FilterSerializer(serializers.Serializer):
        location = serializers.CharField(required=False, max_length=100)

    class HotelOutputSerializer(serializers.ModelSerializer):
        rooms = serializers.SerializerMethodField('rooms_count')

        class Meta:
            model = Hotel
            fields = ["id", "name", "location", "rooms"]

        def rooms_count(self, hotel):
            return hotel.rooms.all().count()


    @extend_schema(
            parameters=[FilterSerializer],
            responses=HotelOutputSerializer,
        )
    def get(self, request):
        query = hotel_list()
        filterset = self.filterset_class(data=request.query_params, queryset=query)
        if filterset.is_valid():
            query = filterset.qs
        paginator = self.pagination_class()
        paginated_query = paginator.paginate_queryset(query, request)
        serializer = self.HotelOutputSerializer(paginated_query, many=True)
        return paginator.get_paginated_response(serializer.data)




class HotelDetailApi(ApiAuthMixin, APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter
    pagination_class = CustomPagination
    
    class FilterSerializer(serializers.Serializer):
        capacity__gte = serializers.IntegerField(required=False)
        capacity__lte = serializers.IntegerField(required=False)


    class HotelDetailOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = "__all__"

    
    @extend_schema(
            parameters=[FilterSerializer],
            responses=HotelDetailOutputSerializer
        )
    def get(self, request, hotel_id):
        query = room_list(hotel_id=hotel_id)
        filterset = self.filterset_class(data=request.query_params, queryset=query)
        if filterset.is_valid():
            query = filterset.qs
        paginator = self.pagination_class()
        paginated_query = paginator.paginate_queryset(query, request)
        serializer = self.HotelDetailOutputSerializer(paginated_query, many=True)
        return paginator.get_paginated_response(serializer.data)
    


class RoomDetailApi(ApiAuthMixin, APIView) :

    class OutputRoomSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = "__all__"


    @extend_schema(responses=OutputRoomSerializer)
    def get(self, request, room_id):
        query = get_room(room_id=room_id)
        serializer = self.OutputRoomSerializer(query)
        return Response(serializer.data)



class BookingApi(ApiAuthMixin, APIView):

    pagination_class = CustomPagination
    
    class OutputBookingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Booking
            fields = "__all__"

    @extend_schema(responses=OutputBookingSerializer)
    def get(self, request):
        query = booking_list(user=request.user)
        paginator = self.pagination_class()
        paginated_query = paginator.paginate_queryset(query, request)
        serializer = self.OutputBookingSerializer(paginated_query, many=True)
        return paginator.get_paginated_response(serializer.data)
    




class BookingDetailApi(ApiAuthMixin, APIView):

    def delete(self, request, booking_id):

        try:
            booking = get_booking(user=request.user, booking_id=booking_id)

            if (booking.start_time - now()) > timedelta(days=2):
                unbooking(booking_id=booking_id)
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response({"error": "Cannot cancel booking within 2 days of start time."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)




class RoomBookingApi(ApiAuthMixin, APIView):

    pagination_class = CustomPagination

    class InputBookingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Booking
            fields = ('start_time', 'end_time',)

        def validate(self, data):
            room_id = self.context.get('room_id')
            bookings = Booking.objects.filter(
                room_id=room_id,
                start_time__lt=data.get('end_time'),
                end_time__gt=data.get('start_time'),
            )
            if data.get('start_time') < now() :
                raise serializers.ValidationError("Start time must be valid.")
            elif data.get('start_time') >= data.get('end_time'):
                raise serializers.ValidationError("End time must be after start time.")
            elif bookings.exists():
                raise serializers.ValidationError("Room is not available for the specified time range.")
            
            return data

    
    class OutputBookingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Booking
            fields = "__all__"


    @extend_schema(responses=OutputBookingSerializer)
    def get(self, request, room_id):
        query = room_booking_list(user=request.user, room_id=room_id)
        paginator = self.pagination_class()
        paginated_query = paginator.paginate_queryset(query, request)
        serializer = self.OutputBookingSerializer(paginated_query, many=True)
        return paginator.get_paginated_response(serializer.data)


    @extend_schema(request=InputBookingSerializer, responses=OutputBookingSerializer)
    def post(self, request, room_id):
        serializer = self.InputBookingSerializer(data=request.data, context={'room_id':room_id})
        serializer.is_valid(raise_exception=True)
        
        try:
            booking = create_booking(
                user=request.user,
                room_id=room_id, 
                start_time=serializer.validated_data.get('start_time'), 
                end_time=serializer.validated_data.get('end_time')
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputBookingSerializer(booking, context={'request':request}).data)

    