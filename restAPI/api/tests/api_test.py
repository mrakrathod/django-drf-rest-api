import json
from rest_framework.test import APIClient
from unittest import TestCase
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserRegistrationAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.valid_payload = {
            "first_name": "Johnuser",
            "last_name": "Muflar",
            "email": "john@test.com",
            "username": "john",
            "user_password": "123654789"
        }

        self.invalid_payload = {
            "first_name": "Johnuser",
            "last_name": "Muflar",
            "email": "john@test.com",
            "username": "",
            "user_password": "123654789"
        }

        self.allready_register_payload = {
            "first_name": "Johnuser",
            "last_name": "Muflar",
            "email": "john@test.com",
            "username": "john",
            "user_password": "123654789"
        }

        self.api_endpoint = '/api/v1/register/'

        self.success_msg = 'Successfully register new user.'
        self.invaid_message = 'This field may not be blank.'
        self.registered_user = 'A user with that username already exists.'


    def test_register_user(self):

        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], self.success_msg)


    def test_register_user_invalid(self):
        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], self.invaid_message)


    def test_user_allredy_register(self):
        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.allready_register_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], self.registered_user)


class UserLoginAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        user, created = User.objects.get_or_create(username='johnuser', password='1234569870')
        user.set_password(user.password)
        user.save()

        self.valid_payload = {
            "username": "johnuser",
            "password": "1234569870"
        }

        self.api_endpoint = '/api/v1/login'

        self.success_msg = 'Successfully login.'

    def test_authenticate_user_login(self):

        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.success_msg)



class UserLogOutAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        user, created = User.objects.get_or_create(username='johnuser1', password='1234569870')
        user.set_password(user.password)
        user.save()
        token = Token.objects.create(user=user)

        self.valid_payload = {
            "token": token.key,
        }

        self.api_endpoint = '/api/v1/logout'

        self.success_msg = 'Successfully logout.'

    def test_authenticate_user_login(self):

        response = self.client.post(
            self.api_endpoint,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.success_msg)

