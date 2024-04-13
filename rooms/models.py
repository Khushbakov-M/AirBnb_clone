from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image

class Room(models.Model):
    class Meta:
        ordering = ["-id"]

    name = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    price = models.IntegerField(help_text="USD per night")
    beds = models.IntegerField(default=1)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    check_in = models.TimeField(default="00:00:00")
    check_out = models.TimeField(default="00:00:00")
    instant_book = models.BooleanField(default=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )

    def __str__(self):
        return self.name

    def photo_number(self):
        return self.photos.count()

    photo_number.short_description = "Photo Count"


class Photo(models.Model):

    file = models.ImageField()
    room = models.ForeignKey(
        "rooms.Room", related_name="photos", on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=140)

    def clean(self):
        if self.file:
            try:
                # Open the image file to check its validity
                img = Image.open(self.file)
            except Exception as e:
                raise ValidationError("Invalid file: Please upload a valid image file.")

    def __str__(self):
        return self.room.name