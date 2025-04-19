from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule
from .serializers import ScheduleSerializer

@api_view(['GET'])
def get_schedules(request):
    schedules = Schedule.objects.all().order_by('-created_at') 
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_default_schedule(request):
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        date = serializer.validated_data.get('date')
        day_of_week = serializer.validated_data.get('day_of_week')
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')

        exact_exists = Schedule.objects.filter(
            date=date,
            day_of_week =day_of_week ,
            start_time=start_time,
            end_time=end_time
        ).exists()

        if exact_exists:
            return Response(
                {"error": f"{date} {start_time}-{end_time} is already scheduled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
