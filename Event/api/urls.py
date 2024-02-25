from django.contrib import admin
from django.urls import path
from .views import (EventViewSet, UserListView, SignupEventView,
                    EventsMyViewSet)

app_name = 'Event:api'
urlpatterns = [

    path('events/', EventViewSet.as_view(), name='event_list'),
    path('users/', UserListView.as_view(), name='user-list'),

    path('event/<int:id>/', SignupEventView.as_view(), name='signup-event'),
    path('events/my/', EventsMyViewSet.as_view(), name='events')
]
