from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from meeting import views
from django.conf.urls import include

urlpatterns = [
    path('users/', views.UsersList.as_view()),
    path('users/<int:pk>/', views.UsersDetail.as_view()),
    path('meetings/', views.MeetingsList.as_view()),
    path('meetings/<int:pk>/', views.MeetingsDetail.as_view()),
    path('meetingRooms/', views.MeetingRoomsList.as_view()),
    path('meetingRooms/<int:pk>/', views.MeetingRoomsDetail.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)