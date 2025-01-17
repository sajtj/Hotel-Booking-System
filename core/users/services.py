from django.db import transaction
from .models import BaseUser, Profile

def create_user(*, email:str, password:str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)

def create_profile(*, user:BaseUser) -> Profile:
    return Profile.objects.create(user=user)

@transaction.atomic
def register(*, email:str, password:str) -> BaseUser:
    user = create_user(email=email, password=password)
    create_profile(user=user)

    return user