from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Speak
from .serializers import SpeakSerializer


class ListCreateSpeakView(ListCreateAPIView):
    model = Speak
    serializer_class = SpeakSerializer

    def get_queryset(self):
        return Speak.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = SpeakSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new Speak successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Speak unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
#
# class UpdateDeleteCarView(RetrieveUpdateDestroyAPIView):
#     model = Car
#     serializer_class = CarSerializer
#
#     def put(self, request, *args, **kwargs):
#         car = get_object_or_404(Car, id=kwargs.get('pk'))
#         serializer = CarSerializer(post, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return JsonResponse({
#                 'message': 'Update Car successful!'
#             }, status=status.HTTP_200_OK)
#
#         return JsonResponse({
#             'message': 'Update Car unsuccessful!'
#         }, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         car = get_object_or_404(Car, id=kwargs.get('pk'))
#         car.delete()
#
#         return JsonResponse({
#             'message': 'Delete Car successful!'
#         }, status=status.HTTP_200_OK)
