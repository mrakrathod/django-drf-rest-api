# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import UserRegistrationSerializer, AuthTokenSerializer, UserLogoutSerializer


class UserRegistrationViewset(viewsets.ModelViewSet):
    """
    It's user registration API to register new user.
    """
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request):
        """
            URL : /api/v1/register/
            Endpoints : /register/
            Accepted Method : POST

            Accepted Param in body:
             {
                "first_name": "",
                "last_name": "",
                "email": "",
                "username": "",
                "user_password": ""
            }

            Accepted success response: 
            {
                "status": 201,
                "message": "Successfully register new user.",
                "token": "ce80f75182ae74bf851d3d7d32941152ed43521e"
            }
        """
        serializer = self.serializer_class(data=request.data)
        # check serializer is valid or not.
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            return Response({
                    'status': status.HTTP_201_CREATED,
                    'message': 'Successfully register new user.',
                    'token': user.auth_token.key ,
                })


class ObtainUserAuthToken(APIView):
    """
    IT's user login view. accepted method post. it's return always new token.
        URL : /api/v1/login/
        Endpoints : /login/
        Accepted Method : POST

        Accepted Param in body:
        {
            "username": "",
            "password": ""
        }

        Accepted success response: 
        {
            "status": 201,
            "message": "Successfully login.",
        }      
    """
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            try:
                user.auth_token.delete()
            except Exception as e:
                pass

            # create new token.
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "status": status.HTTP_200_OK,
                "token": token.key,
                "message" : 'Successfully login.'
            })

class UserLogout(APIView):
    """
    IT's user logout view. accepted method post.
        URL : /api/v1/logout/
        Endpoints : /logout/
        Accepted Method : POST

        Accepted Param in body:
        {
            "token": ""
        }

        Accepted success response: 
        {
            "status": 200,
            "message": "Successfully logout."
        } 
    """
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        token.delete()

        return Response({
            "status": status.HTTP_200_OK,
            "message": 'Successfully logout.'
        })

