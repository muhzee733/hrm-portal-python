from django.urls import path
from .views import create_default_schedule, get_schedules

urlpatterns = [
    path('create-schedule/', create_default_schedule),
    path('schedules/', get_schedules),
]
