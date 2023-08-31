from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True)
    superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField('rooms.Room', related_name='favs')

    def room_count(self):
        return self.rooms.count()
    
    room_count.short_description = 'Room Count'