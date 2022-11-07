from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='profile_image/')
    bio = models.TextField(null=True, blank=True)


class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follows {self.to_user}'
