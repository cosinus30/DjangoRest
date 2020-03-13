# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from meeting.models import User, Meeting, MeetingRoom
from meeting.serializers import UserSerializer, MeetingSerializer, MeetingRoomSerializer
from meeting.permissions import IsOwnerOrReadOnly

from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import permissions

# v3
# from rest_framework import mixins
# from rest_framework import generics

from rest_framework import generics

# Create your views here.

# it is the way of creating views without REST framework.
# @csrf_exempt
# def users_list(request):
#     """
#     List all users, or create a new user.
#     """

#     if request.method == 'GET':
#         users = Users.objects.all()
#         serializer = UsersSerializer(users, many=True)
#         return JsonResponse(serializer.data, safe = False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = UsersSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201)
#         return JsonResponse(serializer.errors, status = 400)


# Again without REST framework
# @csrf_exempt
# def users_detail(request, pk):
#     """
#     Retrieve, update, or delete a code snippet.
#     """
#     try:
#         user = Users.objects.get(pk=pk)
#     except Users.DoesNotExist:
#         return HttpResponse(status=404)
    
#     if request.method == 'GET':
#         serializer = UsersSerializer(user)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = UsersSerializer(user, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status = 400)

#     elif request.method == 'DELETE':
#         user.delete()
#         return HttpResponse(status = 204)


# v2
# class UsersList(APIView):
#     """
#     List all users or create a new user.
#     """
#     def get(self, request, format = None):
#         users = Users.objects.all()
#         serializer = UsersSerializer(users, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format = None):
#         serializer = UsersSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# class UsersDetail(APIView):
#     """
#     Retrieve, update or delete a user.
#     """
#     def get_object(self, pk):
#         try:
#             user = Users.objects.get(pk=pk)
#         except Users.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk, format = None):
#         user = self.get_object(pk)
#         serializer = UsersSerializer(user)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format = None):
#         user = self.get_object(pk)
#         serializer = UsersSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format = None):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status = status.HTTP_204_NOT_CONTENT)


# v3
# class UsersList(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class UsersDetail(mixins.RetrieveModelMixin,
#                   mixins.DestroyModelMixin,
#                   mixins.UpdateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MeetingsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)

    def get(self, request, format = None):
        meetings = Meeting.objects.all()
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)
    
    def post(self, request, format = None):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            serializer.save()
            if serializer.data['meeting_id'] == 0:
                print(serializer.data)
                return Response({"Failed: Confliction"}, status = status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class MeetingsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class MeetingRoomsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)

class MeetingRoomsDetail(generics.RetrieveUpdateDestroyAPIView):
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
