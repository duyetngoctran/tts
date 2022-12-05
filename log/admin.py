from django.contrib import admin
from .models import Speak

class SpeakAdmin(admin.ModelAdmin):
    list_display = ('username', 'txt', 'timestamp')
    #list_display = [field.name for field in Setting._meta.get_fields()]

admin.site.register(Speak, SpeakAdmin)

