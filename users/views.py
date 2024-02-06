from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework import serializers
from rest_framework import status

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
        'Update': '/update/pk',
        'Delete': '/user/pk/delete'
    }
    return Response(api_urls)

@api_view(['POST'])
def add_users(request):
    """
    API endpoint for adding new users.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing user data if the user is created successfully,
                  or error messages if validation fails.
    """
    user = UserSerializer(data=request.data)

    # Check if a user with the same data already exists
    if CustomUser.objects.filter(username=request.data.get('username'),email=request.data.get('email'),phone_number=request.data.get('phone_number')):
        raise serializers.ValidationError('User with this data already exists')

    if user.is_valid():
        user.save()
        return Response(user.data, status=status.HTTP_201_CREATED)
    else:
        return Response(user.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_users(request):
    """
    API endpoint for viewing users.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing serialized user data.
    """
    # Filter users based on query parameters if provided
    if request.query_params:
        users = CustomUser.objects.filter(**request.query_params.dict())
    else:
        users = CustomUser.objects.all()

    if users:
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_users(request, pk):
    """
    API endpoint for updating a user.

    Args:
        request (Request): The incoming request.
        pk (int): The primary key of the user to be updated.

    Returns:
        Response: A response containing updated user data if successful, or error messages if validation fails.
    """
    try:
        user = CustomUser.objects.get(pk=pk)
        data = UserSerializer(instance=user, data=request.data)
    except Exception as e:
        response_html = f'Error: {str(e)}'
        return Response(response_html, status=status.HTTP_404_NOT_FOUND)

    if data.is_valid():
        data.save()
        return Response(data.data,status.HTTP_200_OK)
    else:
        return Response(data.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_users(request, pk):
    """
    API endpoint for deleting a user.

    Args:
        request (Request): The incoming request.
        pk (int): The primary key of the user to be deleted.

    Returns:
        Response: A response indicating the success or failure of the deletion.
    """
    try:
        user = CustomUser.objects.get(pk=pk)
        user.delete()
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
