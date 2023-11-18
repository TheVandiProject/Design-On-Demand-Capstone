from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializers import UsersSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def users_list(request):
    """
    List all books or create a new book
    """
    if request.method == 'GET':
        books = Users.objects.all()
        serializer = UsersSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    """
    Retrieve, update or delete a book
    """
    try:
        book = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UsersSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UsersSerializer(book, data=request.data)
