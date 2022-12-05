from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('speak/', views.ListCreateSpeakView.as_view()),
]