from django.shortcuts import render
from .serializers import RoomSerializer
from .models import Room
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.
class RoomListView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]