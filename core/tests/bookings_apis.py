# python manage.py test core.tests.bookings_apis 
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.bookings.models import Hotel, Room, Booking

User = get_user_model()

class BookingApiTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email='testuser1@example.com', password='SecureP@ss123')
        self.user2 = User.objects.create_user(email='testuser2@example.com', password='SecureP@ss1234')
        self.hotel = Hotel.objects.create(name='Test Hotel', location='Test Location')
        self.room = Room.objects.create(hotel=self.hotel, capacity=2)
        self.client.force_authenticate(user=self.user1)

    def test_hotel_list(self):
        url = reverse('api:bookings:hotels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_hotel_detail(self):
        url = reverse('api:bookings:hotel-rooms', args=[self.hotel.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_room_detail(self):
        url = reverse('api:bookings:hotel-rooms-detail', args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('capacity', response.data)

    def test_create_booking(self):
        url = reverse('api:bookings:booking-rooms', args=[self.room.id])
        data = {
            'start_time': (now() + timedelta(days=3)).isoformat(),
            'end_time': (now() + timedelta(days=5)).isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)

    def test_cancel_booking(self):
        booking = Booking.objects.create(
            user=self.user1,
            room=self.room,
            start_time=now() + timedelta(days=3),
            end_time=now() + timedelta(days=4),
        )
        url = reverse('api:bookings:booking-detail', args=[booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_booking_cancelation_error(self):
        booking = Booking.objects.create(
            user=self.user1,
            room=self.room,
            start_time=now() + timedelta(days=1),
            end_time=now() + timedelta(days=2),
        )
        url = reverse('api:bookings:booking-detail', args=[booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot cancel booking within 2 days', response.data['error'])

    def test_room_booking_unavailability(self):
        Booking.objects.create(
            user=self.user1,
            room=self.room,
            start_time=now() + timedelta(days=3),
            end_time=now() + timedelta(days=5),
        )
        self.client.force_authenticate(user=self.user2)
        url = reverse('api:bookings:booking-rooms', args=[self.room.id])

        response = self.client.post(url, data={
            "start_time": (now() + timedelta(days=4)).isoformat(),
            "end_time": (now() + timedelta(days=6)).isoformat(),
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
