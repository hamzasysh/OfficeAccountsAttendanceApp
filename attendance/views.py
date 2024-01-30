from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework import serializers
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def ApiOverview(request):
    """
    API endpoint providing an overview of available endpoints.

    Returns:
        Response: A response containing a dictionary of API endpoints and their descriptions.
    """
    api_urls = {
        'Add': '/create',
        'Read': '/all',
        'Update': '/update/<int:pk>',
        'Delete': '/pk/delete'
    }
    return Response(api_urls)

@api_view(['POST'])
def add_attendance(request):
    """
    API endpoint for adding new attendance records.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing attendance data if the record is created successfully,
                  or error messages if validation fails.
    """
    attendance = AttendanceSerializer(data=request.data)

    # Check if attendance record with the same date and employee already exists
    if Attendance.objects.filter(date=request.data.get('date'), employee=request.data.get('employee')):
        raise serializers.ValidationError('Attendance already exists')

    if attendance.is_valid():
        attendance.save()
        return Response(attendance.data,status=status.HTTP_201_CREATED)
    else:
        return Response(attendance.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_attendance(request):
    """
    API endpoint for viewing attendance records.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing serialized attendance data.
    """
    # Filter attendance records based on query parameters if provided
    if request.query_params:
        try:
            attendance = Attendance.objects.filter(**request.query_params.dict())
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        attendance = Attendance.objects.all()

    if attendance:
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_attendance(request, pk):
    """
    API endpoint for updating an attendance record.

    Args:
        request (Request): The incoming request.
        pk (int): The primary key of the attendance record to be updated.

    Returns:
        Response: A response containing updated attendance data if successful, or error messages if validation fails.
    """
    try:
        attendance = Attendance.objects.get(pk=pk)
        data = AttendanceSerializer(instance=attendance, data=request.data)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if data.is_valid():
        data.save()
        return Response(data.data,status=status.HTTP_200_OK)
    else:
        return Response(data.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_attendance(request, pk):
    """
    API endpoint for deleting an attendance record.

    Args:
        request (Request): The incoming request.
        pk (int): The primary key of the attendance record to be deleted.

    Returns:
        Response: A response indicating the success or failure of the deletion.
    """
    try:
        attendance = Attendance.objects.get(pk=pk)
        attendance.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        response_html = f'Error: {str(e)}'
        return Response(response_html,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def hello_message(request):
    """
    API endpoint returning a simple hello message.

    Returns:
        Response: A response containing a dictionary with a hello message.
    """
    content = {'message': 'Hello, World!'}
    return Response(content)
