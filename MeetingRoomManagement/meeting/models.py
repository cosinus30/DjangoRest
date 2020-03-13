from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Meeting(models.Model):
    meeting_title = models.CharField(max_length = 50, blank = True, default = 'Title is not given')
    meeting_estimated_time = models.DurationField(blank = False, null = False)
    meeting_date = models.DateTimeField(blank = False, null = False)
    meeting_ending_time = models.DateTimeField(blank = True, null = True) # It is always set on serializer. 
    meeting_id = models.AutoField(primary_key = True)
    creator = models.ForeignKey('User', related_name = 'created_meetings', on_delete = models.CASCADE,)
    meeting_room = models.ForeignKey('MeetingRoom',related_name = 'meeting_room', on_delete = models.CASCADE,)

class MeetingRoom(models.Model):
    meeting_room_id = models.AutoField(primary_key = True)
    meeting_room_availability = models.BooleanField(default = True, null = False)
    meeting_room_capacity = models.IntegerField(null = False, blank = False)
    meeting_room_name = models.CharField(max_length = 50, null = False)
    creator = models.ForeignKey('User', related_name = 'created_rooms', on_delete = models.CASCADE,) # Admin user can create new rooms, update rooms. 

class User(AbstractUser):
    position = models.CharField(max_length = 50, null = False)
    meetings = models.ManyToManyField(Meeting, blank = True, null = True)

