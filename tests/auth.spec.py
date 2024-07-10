import json

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from jwt import decode
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Organisation, User

# Create your tests here.

jwt_decode_handler = JWTAuthentication()


class UserRegistrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "08012345678"
        }
        self.user_data2 = {
            "firstName": "James",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "08012345678"
        }

    def test_register_email_validation_error(self):
        invalid_data = self.user_data.copy()
        invalid_data['email'] = ''
        response = self.client.post(self.register_url,
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_register_firstName_validation_error(self):
        invalid_data = self.user_data.copy()
        invalid_data['firstName'] = ''
        response = self.client.post(self.register_url,
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_register_lastName_validation_error(self):
        invalid_data = self.user_data.copy()
        invalid_data['lastName'] = ''
        response = self.client.post(self.register_url,
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_register_password_validation_error(self):
        invalid_data = self.user_data.copy()
        invalid_data['password'] = ''
        response = self.client.post(self.register_url,
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_register_user_success(self):
        response = self.client.post(self.register_url,
                                    data=json.dumps(self.user_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])

    def test_repeat_email_validation_error(self):
        self.client.post(self.register_url,
                         data=json.dumps(self.user_data),
                         content_type='application/json')
        response = self.client.post(self.register_url,
                                    data=json.dumps(self.user_data2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user with this email already exists.',
                      response.data['errors']['email'])


class UserLoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "08012345678"
        }
        self.client.post(self.register_url,
                         data=json.dumps(self.user_data),
                         content_type='application/json')

    def test_login_incorrect_email(self):
        response = self.client.post(self.login_url,
                                    data=json.dumps({
                                        "email": "incorrectemail",
                                        "password": self.user_data['password']
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Authentication failed')

    def test_login_incorrect_password(self):
        response = self.client.post(self.login_url,
                                    data=json.dumps({
                                        "email": self.user_data['email'],
                                        "password": "incorrectpassword"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Authentication failed')

    def test_login_user_success(self):
        response = self.client.post(self.login_url,
                                    data=json.dumps({
                                        "email": self.user_data['email'],
                                        "password": self.user_data['password']
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])


class TokenGeneratinTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "08012345678"
        }
        self.response = self.client.post(self.register_url,
                                    data=json.dumps(self.user_data),
                                    content_type='application/json'
                                    )
        self.token = self.response.data['data']['accessToken']

    def test_token_contains_correct_user_details(self):
        # authenticated_user, decoded_token = jwt_decode_handler.authenticate(request=None, user=self.token)
        decoded_token = decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded_token['user_id'], self.user_data['email'])
        self.assertIn('exp', decoded_token)


class OrganisationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.orgs_url = reverse('organisations')
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.user_data2 = {
            "firstName": "James",
            "lastName": "Deran",
            "email": "james@example.com",
            "password": "password456",
            "phone": "0987654321"
        }
        response = self.client.post(self.register_url,
                                    data=json.dumps(self.user_data),
                                    content_type='application/json')
        
        self.user1 = response.data['data']
        
        res = self.client.post(self.register_url,
                         data=json.dumps(self.user_data2),
                         content_type='application/json')
        
        self.user2 = res.data['data']
        

    def test_user_cannot_access_other_users_organisation(self):
        
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.user1['accessToken']}"}
        response = self.client.get(self.orgs_url, **headers)
        user1_org = response.data['data']['organisations']
        
        # self.client.headers = {"Authorization": f"Bearer {self.token}"}
        # response = self.client.get(self.orgs_url)
        
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user1_org), 1)
        
        user2_org = Organisation.objects.create(name="Jame's Organisation", owner=User(**self.user2['user']))
        
        response = self.client.get(reverse('org_details', args=[user2_org.orgId]), **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
