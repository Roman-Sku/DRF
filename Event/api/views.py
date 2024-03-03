from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from Event.cache import get_cached
from Event.models import Event, User
from . import permissions
from .serializers import EventSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class EventsMyViewSet(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user)


class SignupEventView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get(self, request, id):
        event = get_object_or_404(Event, pk=id, meeting_time__gt=timezone.now())
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def post(self, request, id, **kwargs, ):
        event = get_object_or_404(Event, pk=id, meeting_time__gt=timezone.now())
        event.users.add(request.user)
        return Response({"message": "Successfully subscribed to the event"})


def get_token(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {"refresh": str(refresh), "access": str(access)}


class UserListView(ListAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({'serializer': serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({**serializer.data}, status=201)
        return Response(serializer.errors)


class EventViewSet(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Event.objects.filter(meeting_time__gt=timezone.now())
        return get_cached("events", queryset, 300)
