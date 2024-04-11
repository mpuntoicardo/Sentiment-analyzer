from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import UserSerializer, SearchSerializer, UrlSerializer, KeywordSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import logout


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Search

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(str(request.data['password'])):
        return Response({"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"message":"Login succesful","token": token.key}, status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User(
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data.get('first_name', ''),
            email=serializer.validated_data['email'],
        )
        user.set_password(str(serializer.validated_data['password']))
        user.save()
        serializer = UserSerializer(instance=user)
        return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"message": "Error creating user", "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"message":"Token correctly verified", "user":{
        "email": request.user.email,
        "id": request.user.id,
        "name": request.user.first_name
    }})

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({"message":"User logged out correctly", "user":{
        "email": request.user.email,
        "id": request.user.id
    }})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_search_id(request):
    userId = request.user.id
    searchs = Search.objects.filter(created_by=userId)
    serializer = SearchSerializer(searchs, many=True)
    return Response({"message": "Searchs found correctly", "searchs": serializer.data})

#Turns a search from favorite to not and vice versa
@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_search_is_favorite(request, id):
    userId = request.user.id
    user = User.objects.get(id = userId)
    search = get_object_or_404(Search, created_by= userId, id= id)
    search.is_favorite = None if search.is_favorite is not None else user
    search.save()
    serializer = SearchSerializer(search)
    return Response({"message":"Search updated successfully", "search": serializer.data})