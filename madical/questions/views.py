# views.py

from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer, PatientQuestionSerializer
from .models import Question, PatientQuestion

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Question added successfully.",
        }, status=status.HTTP_201_CREATED)
    return Response({
        "message": "Validation failed.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQuestions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_patient(request):
    data = request.data

    # Check if email already exists
    if get_user_model().objects.filter(email=data['email']).exists():
        return Response({"message": "Email already registered!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create user (patient)
        patient = get_user_model().objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']  # Password should be hashed automatically
        )
    except Exception as e:
        return Response({"message": "Error creating patient", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Save Patient's Answers to Questions
    try:
        patient_questions = []
        for q_data in data['questions']:  # Loop through the answers
            question = Question.objects.get(id=q_data['question_id'])  # Get the question by ID
            patient_questions.append(PatientQuestion(
                patient=patient,  # Link to the patient who is answering
                question=question,  # Link to the question
                answer=q_data['answer']  # Store the answer provided
            ))

        # Bulk save all patient answers
        PatientQuestion.objects.bulk_create(patient_questions)

        return Response({"message": "Patient registered and answers saved successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"message": "Error saving answers", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
