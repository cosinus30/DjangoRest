from rest_framework import serializers
from meeting.models import Meeting, MeetingRoom, User
import datetime
from rest_framework import status
from rest_framework.response import Response

class MeetingRoomSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source = 'creator.username')
    class Meta:
        model = MeetingRoom
        fields = ['meeting_room_id','meeting_room_availability','meeting_room_capacity','meeting_room_name','creator']


class UserSerializer(serializers.ModelSerializer):
    created_meetings = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    created_rooms = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only':True}}
        fields = ['id','first_name','last_name','email','username','password', 'position','created_meetings', 'meetings', 'created_rooms']
    def create(self, validated_data):
        user = User(
            first_name = validated_data.get('first_name',None),
            last_name = validated_data.get('last_name',None),
            email = validated_data.get('email',None),
            username = validated_data.get('username',None),
            position = validated_data.get('position',None),
        )
        user.set_password(validated_data.get('password',None))
        user.save()
        # list yapmak icin * ekle
        user.meetings.add(*validated_data.get('meetings',None)) 
        return user

class MeetingSerializer(serializers.ModelSerializer):   
    creator = serializers.ReadOnlyField(source = 'creator.username')
    class Meta:
        model = Meeting
        fields = ['meeting_id','meeting_title', 'meeting_estimated_time', 'meeting_date', 'meeting_room', 'creator', 'user_set',]
    def create (self, validated_data):
        meeting = Meeting(
            meeting_id = validated_data.get('meeting_id',None),
            meeting_title = validated_data.get('meeting_title',None),
            meeting_estimated_time = validated_data.get('meeting_estimated_time',None),
            meeting_date = validated_data.get('meeting_date', None),           
            meeting_room = validated_data.get('meeting_room',None),
            creator = validated_data.get('creator',None),
            meeting_ending_time = validated_data.get('meeting_date', None) + validated_data.get('meeting_estimated_time',None)
        )
        todays_meetings = Meeting.objects.filter(meeting_date__day = meeting.meeting_date.strftime('%d')).filter(meeting_room = meeting.meeting_room)
        is_appropriate = True
        for current_meeting in todays_meetings:
            if current_meeting.meeting_ending_time >= meeting.meeting_ending_time and meeting.meeting_ending_time >= current_meeting.meeting_date:
                is_appropriate = False
                print("if1")
            elif current_meeting.meeting_ending_time >= meeting.meeting_ending_time and meeting.meeting_date >= current_meeting.meeting_date:
                is_appropriate = False
                print("if2")
            elif meeting.meeting_date >= current_meeting.meeting_date and meeting.meeting_date <= current_meeting.meeting_ending_time:
                is_appropriate = False
                print("if3")
        serializer = MeetingSerializer(data=validated_data)
        if is_appropriate:
            meeting.save()
            meeting.user_set.add(*validated_data.get('user_set',None)) 
            return meeting
        else:
            print("Meeting id is set to 0")
            meeting.meeting_id = 0
            return meeting
    
    def update(self, instance, validated_data):
        instance.meeting_id = validated_data.get('meeting_id',instance.meeting_id)
        instance.meeting_title = validated_data.get('meeting_title',instance.meeting_title)
        instance.meeting_estimated_time = validated_data.get('meeting_estimated_time',instance.meeting_estimated_time)
        instance.meeting_date = validated_data.get('meeting_date', instance.meeting_date)
        instance.meeting_room = validated_data.get('creator',instance.meeting_room)
        instance.creator = validated_data.get('creator',instance.creator)
        instance.meeting_ending_time = instance.meeting_date + instance.meeting_estimated_time
        
        todays_meetings = Meeting.objects.filter(meeting_date__day = instance.meeting_date.strftime('%d')).filter(meeting_room = instance.meeting_room).exclude(meeting_id = instance.meeting_id).filter(meeting_date__month = instance.meeting_date.strftime('%m'))
        is_appropriate = True
        for current_meeting in todays_meetings:
            print(current_meeting.meeting_ending_time)
            print(instance.meeting_ending_time)
            if current_meeting.meeting_ending_time >= instance.meeting_ending_time and instance.meeting_ending_time >= current_meeting.meeting_date:
                is_appropriate = False
            elif current_meeting.meeting_ending_time >= instance.meeting_ending_time and instance.meeting_date >= current_meeting.meeting_date:
                is_appropriate = False
            elif instance.meeting_date >= current_meeting.meeting_date and instance.meeting_date <= current_meeting.meeting_ending_time:
                is_appropriate = False
        serializer = MeetingSerializer(data=validated_data)
        if is_appropriate:
            instance.save()
            instance.user_set.add(*validated_data.get('user_set',instance.user_set)) 
            return instance
        else:
            print("Meeting id is set to 0.2")
            instance.meeting_id = 0
            return instance

    # ModelSerializer class automatically generates the create and update methods.
    # def create (self, validated_data):
    #     """
    #     Create and return a new `Users` instance, given the validated data
    #     """
    #     return Users.objects.create(**validated_data)

    # def update (self, instance, validated_data):
    #     """
    #     Update and return an existing `Users instance`, given the validated data.
    #     """
    #     instance.users_id = validated_data.get('users_id', instance.users_id)
    #     instance.users_first_name = validated_data.get('users_first_name', instance.users_first_name)
    #     instance.users_last_name = validated_data.get('users_last_name', instance.users_last_name)
    #     instance.users_position = validated_data.get('users_position', instance.users_position)
    #     instance.users_username = validated_data.get('users_username', instance.users_username)
    #     instance.users_password = validated_data.get('users_password', instance.users_password)
    #     instance.save()
    #     return instance