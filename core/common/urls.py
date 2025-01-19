from django.urls import path, include

urlpatterns = [
    path('users/', include(('core.users.urls', 'users'))),
    path('auth/', include(('core.authentication.urls', 'auth'))),
    path('bookings/', include(('core.bookings.urls', 'bookings'))),
]