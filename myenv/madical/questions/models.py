from django.db import models

class Question(models.Model):
    QUESTION_TYPES = (
        ('text', 'Text'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
    )

    question = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    choices = models.JSONField(blank=True, null=True) 

    class Meta:
        db_table = 'pre_questions'

    def __str__(self):
        return self.question
