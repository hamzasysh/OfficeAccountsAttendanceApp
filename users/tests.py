from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.models import CustomUser
import uuid
from django.urls import reverse


class UserTests(TestCase):
    """
    Test cases for the CustomUser model and associated API endpoints.
    """

    def setUp(self):
        """
        Set up test data and client credentials.
        """
        self.client = APIClient()
        fake_email = f"{str(uuid.uuid4())}@email.com"
        self.user = CustomUser.objects.create(
            email=str(uuid.uuid4()),
            password="dummye@123",
            department="IT",
            position="PM",
            address="14-A AIT lhr",
            phone_number="+92324567890"
        )
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'department': 'IT',
            'position': 'Developer',
            'date_of_birth': '1990-01-01',
            'address': '123 Main St, City',
            'phone_number': '123-456-7890',
            'joining_date': '2020-01-01',
        }
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_user_model_create_user(self):
        """
        Test creating a user using the CustomUser model.
        """
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.department, self.user_data['department'])
        self.assertEqual(user.position, self.user_data['position'])
        self.assertEqual(str(user.date_of_birth), self.user_data['date_of_birth'])
        self.assertEqual(user.address, self.user_data['address'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        self.assertEqual(str(user.joining_date), self.user_data['joining_date'])

    def test_user_str_representation(self):
        """
        Test the string representation of a user.
        """
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])

    def test_user_create_api_with_correct_data(self):
        """
        Test creating a user through the API with correct data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
            "phone_number": "+92327657890"
        }
        response = self.client.post(reverse('add-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_api_with_incorrect_data(self):
        """
        Test creating a user through the API with incorrect data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
        }
        response = self.client.post(reverse('add-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_view_api_with_correct_data(self):
        """
        Test viewing a user through the API with correct data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
            "phone_number": "+92327657890"
        }
        self.client.post(reverse('add-user'), data, format='json')
        query_params = {'email': 'dummyrat@systems.com'}
        # Using reverse to generate the URL with query parameters
        url_with_query_params = reverse('view-user') + '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])
        response = self.client.get(url_with_query_params, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_view_api_with_incorrect_data(self):
        """
        Test viewing a user through the API with incorrect data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
            "phone_number": "+92327657890"
        }
        self.client.post(reverse('add-user'), data, format='json')
        query_params = {'email': 'dummyraton@systems.com'}
        # Using reverse to generate the URL with query parameters
        url_with_query_params = reverse('view-user') + '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])
        response = self.client.get(url_with_query_params, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update_api_with_correct_data(self):
        """
        Test updating a user through the API with correct data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
            "phone_number": "+92327657890"
        }
        response = self.client.post(reverse('add-user'), data, format='json')
        url = reverse('update-user', kwargs={'pk': response.data['id']})
        data['username'] = "simpleEmployee"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_api_with_incorrect_data(self):
        """
        Test updating a user through the API with incorrect data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
            "phone_number": "+92327657890"
        }
        response = self.client.post(reverse('add-user'), data, format='json')
        url = reverse('update-user', kwargs={'pk': response.data['id'] - 10})
        data['username'] = "simpleEmployee"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_delete_api_with_correct_data(self):
        """
        Test deleting a user through the API with correct data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
            "phone_number": "+92327657890"
        }
        response = self.client.post(reverse('add-user'), data, format='json')
        url = reverse('delete-user', kwargs={'pk': response.data['id']})
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_user_delete_api_with_incorrect_data(self):
        """
        Test deleting a user through the API with incorrect data.
        """
        data = {
            "username": "ratemployee",
            "password": "dummyrate@123",
            "email": "dummyrat@systems.com",
            "department": "IT",
            "position": "PM",
            "address": "14-A AIT lhr",
            "phone_number": "+92327657890"
        }
        response = self.client.post(reverse('add-user'), data, format='json')
        url = reverse('delete-user', kwargs={'pk': response.data['id'] - 10})
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
