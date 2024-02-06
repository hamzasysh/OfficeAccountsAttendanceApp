from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Accounts
from .serializers import AccountSerializer
from rest_framework import serializers
from rest_framework import status
import decimal

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
def add_account(request):
    """
    API endpoint for adding new accounts records.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing accounts data if the record is created successfully,
                  or error messages if validation fails.
    """
    account = AccountSerializer(data=request.data)

    # Check if accounts record for the same employee, year, and month already exists
    if Accounts.objects.filter(employee=request.data.get('employee'),year=request.data.get('year'),month=request.data.get('month')):
        raise serializers.ValidationError('Accounts Record for this employee already exists')

    if account.is_valid():
        try:
            account.save()
        except Exception as e:
            return Response(f"Error saving account: {e}")
        return Response(account.data,status=status.HTTP_201_CREATED)
    else:
        return Response(account.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_account(request):
    """
    API endpoint for viewing accounts records.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing serialized accounts data.
    """
    # Filter accounts records based on query parameters if provided
    if request.query_params:
        account = Accounts.objects.filter(**request.query_params.dict())
    else:
        account = Accounts.objects.all()

    if account:
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_account(request, pk):
    """
    API endpoint for updating an accounts record.

    Args:
        request (Request): The incoming request.
        pk (int): The primary key of the accounts record to be updated.

    Returns:
        Response: A response containing updated accounts data if successful, or error messages if validation fails.
    """
    try:
        account = Accounts.objects.get(pk=pk)
        data = AccountSerializer(instance=account, data=request.data)
    except Exception as e:
        return Response(f'Error: {str(e)}',status=status.HTTP_404_NOT_FOUND)

    if data.is_valid():
        data.save()
        return Response(data.data,status=status.HTTP_200_OK)
    else:
        return Response(data.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_account(request, pk):
    """
    API endpoint for deleting an accounts record.

    Args:
        request (Request): The incoming request.
        pk (int): The primary key of the accounts record to be deleted.

    Returns:
        Response: A response indicating the success or failure of the deletion.
    """
    try:
        account = Accounts.objects.get(pk=pk)
        account.delete()
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
