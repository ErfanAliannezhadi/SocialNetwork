from django.contrib.auth.models import User
from .models import UserProfileModel
from django.db.models.signals import post_save


def create_profile(sender,**kwargs):
    if kwargs['created']:
        UserProfileModel.objects.create(user=kwargs['instance'])


post_save.connect(receiver=create_profile, sender=User)
