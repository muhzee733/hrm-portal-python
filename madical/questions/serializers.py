from rest_framework import serializers
from .models import Question, PatientQuestion

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'type', 'choices']

class PatientQuestionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True)
    
    class Meta:
        model = PatientQuestion
        fields = ['patient', 'question', 'answer', 'role', "frist_name"]