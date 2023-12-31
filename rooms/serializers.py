from rest_framework import serializers
from .models import Room, Photo
from users.serializers import UserSerializer

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ('room,')

class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'url',
            'id',
            'name',
            'address',
            'price',
            'beds',
            'bedrooms',
            'bathrooms',
            'check_in',
            'check_out',
            'instant_book',
            'photos',
            'user',
            'is_fav',
        ]

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError(
                "Check-in and Check-out can't be set the same time"
            )
        return data

    def get_is_fav(self, obj):

        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in request.user.favs.all()
        return False

    def create(self, validated_data):
        request = self.context.get("request")
        room = Room.objects.create(**validated_data, user=request.user)
        return room