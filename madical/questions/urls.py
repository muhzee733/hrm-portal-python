from django.urls import path
from .views import create_question,getQuestions,register_patient

urlpatterns = [
    path('create_questions/', create_question),
    path('questions/', getQuestions),
    path('prequestions/', register_patient, name='pre_questions'),
]
