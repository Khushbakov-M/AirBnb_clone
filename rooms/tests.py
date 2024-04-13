from django.test import TestCase, Client
from users.models import User
from .models import Room, Photo
from django.core.exceptions import ValidationError
import datetime
# Create your tests here
class TestRoomModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='password')
        self.room = Room.objects.create(
            name='A',
            address='T',
            price=500,
            user=self.user,
        )

    def test_isinstance(self):
        self.assertTrue(isinstance(self.room, Room))

    def test_field_validation(self):
        self.room.name *= 141
        with self.assertRaises(ValidationError):
            self.room.full_clean()
        self.assertEquals(self.room.beds, 1)
        self.assertEquals(self.room.bedrooms, 1)
        self.assertEquals(self.room.bathrooms, 1)
        self.assertEquals(self.room.check_in, datetime.time(0, 0))
        self.assertEquals(self.room.check_out, datetime.time(0, 0))
        self.assertEquals(self.room.instant_book, False)

    def test_str_method(self):
        self.assertEquals(str(self.room), self.room.name)

    def test_photo_number_function(self):
        number_of_photos = self.room.photo_number()
        actual_number = Photo.objects.filter(room=self.room).count()
        self.assertEquals(number_of_photos, actual_number)

    def test_room_has_multiple_photos(self):
        Photo.objects.create(room=self.room, file='example.jpg', caption='Test1')
        Photo.objects.create(room=self.room, file='example2.jpg', caption='Test2')
        photos = self.room.photo_number()
        self.assertEquals(photos, 2)

    def test_save_method(self):
        room = Room(
            name='B',
            address='C',
            price=250,
            user=self.user,
        )
        try:
            room.save()
        except Exception as e:
            self.fail(f'Saving Room failed with error: {e}')

        saved_room = Room.objects.get(pk=room.pk)
        self.assertEquals(saved_room.name, 'B')
        self.assertEquals(saved_room.address, 'C')

    def test_instant_book(self):
        self.assertEquals(self.room.instant_book, False)

class TestPhotoModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='password')
        self.room = Room.objects.create(
            name='A',
            address='T',
            price=500,
            user=self.user,
        )
        self.photo = Photo.objects.create(room=self.room, file='example.jpg', caption='For Testing')


    def test_isinstance(self):
        self.assertTrue(isinstance(self.photo, Photo))

    def test_str_method(self):
        self.assertEquals(str(self.photo), self.photo.room.name)

    def test_field_validation(self):
        invalid_file = Photo.objects.create(room=self.room, file='example.txt', caption='For Testing')
        with self.assertRaises(ValidationError):
            invalid_file.full_clean()
        invalid_caption = Photo.objects.create(room=self.room, file='example.jpg', caption='A'*141)
        with self.assertRaises(ValidationError):
            invalid_caption.full_clean()

    def test_save_method(self):
        photo = Photo(
            room=self.room,
            file='example.jpg',
            caption='For Testing',
        )
        try:
            photo.save()
        except Exception as e:
            self.fail(f'Saving Room failed with error: {e}')

        saved_photo = Photo.objects.get(pk=photo.pk)
        self.assertEquals(saved_photo.file, 'example.jpg')
        self.assertEquals(saved_photo.caption, 'For Testing')
