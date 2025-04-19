from django.urls import path
from .views import create_question,getQuestions

urlpatterns = [
    path('create_questions/', create_question),
    path('questions/', getQuestions),
]
