from django.contrib.auth import get_user_model
User = get_user_model()
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
def getQuestions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_patient(request):
    data = request.data
    email = data.get('email')
    role = data.get('role', 'patient') 
    password = data.get('password')
    full_name = data.get('full_name', '')
    first_name = full_name.split(' ')[0]
    last_name = ' '.join(full_name.split(' ')[1:]) if len(full_name.split(' ')) > 1 else ''

    if not email or not password:
        return Response({"message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"message": "Email already registered!"}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 6:
        return Response({"message": "Password must be at least 6 characters long."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = User.objects.create_user(
        username=full_name,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role
)

    except Exception as e:
        return Response({"message": "Error creating patient", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient_questions = []
        for q_data in data.get('questions', []):
            question_id = q_data.get('question_id')
            answer = q_data.get('answer')

            patient_question = PatientQuestion(
                patient=patient, 
                question_id=question_id, 
                answer=answer
            )
            patient_questions.append(patient_question)


        PatientQuestion.objects.bulk_create(patient_questions)
            
        return Response({"message": "Patient registered and answers saved successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "message": "Error saving answers",
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
