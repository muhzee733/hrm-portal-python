from django.db import models
from django.conf import settings
import uuid

class Question(models.Model):
    QUESTION_TYPES = (
        ('text', 'Text'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    choices = models.JSONField(blank=True, null=True) 

    class Meta:
        db_table = 'pre_questions'

    def __str__(self):
        return self.question

class PatientQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'patient_questions'

    def __str__(self):
        return f"{self.patient.username} - {self.question.question}"