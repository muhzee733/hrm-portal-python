from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('questions.urls')),
    path('api/v1/', include('schedule.urls')),
    path('api/v1/', include('authentication.urls')),
]
