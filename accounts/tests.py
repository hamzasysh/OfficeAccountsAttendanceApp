from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.models import CustomUser
from accounts.models import Accounts
import uuid
from django.urls import reverse

class AccountTests(TestCase):
    """
    Test cases for the `Accounts` model and associated APIs.
    """

    def setUp(self):
        """
        Set up the test environment with necessary data.
        """
        self.client = APIClient()

        # Create a fake user for testing
        fake_email = f"{str(uuid.uuid4())}@email.com"
        self.user = CustomUser.objects.create(
            email=fake_email,
            password="dummye@123",
            department="IT",
            position="PM",
            address="14-A AIT lhr",
            phone_number="+92324567890"
        )

        # Data for testing
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

        # Set authentication credentials
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_account_model_create_account(self):
        """
        Test creating an account using the `Accounts` model.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        account = Accounts.objects.create(**data)
        self.assertEqual(account.employee, data['employee'])
        self.assertEqual(account.month, data['month'])
        self.assertEqual(account.year, data['year'])
        self.assertEqual(account.salary, data['salary'])

    def test_account_str_representation(self):
        """
        Test the string representation of the `Accounts` model.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        account = Accounts.objects.create(**data)
        expected_str = f"{account.employee.username} - {account.month}/{account.year} - Salary: {account.salary}"
        self.assertEqual(str(account), expected_str)

    def test_account_create_api_with_correct_data(self):
        """
        Test creating an account via API with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        response = self.client.post(reverse('add-account'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_account_create_api_with_incorrect_data(self):
        """
        Test creating an account via API with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        response = self.client.post(reverse('add-account'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_account_view_api_with_correct_data(self):
        """
        Test viewing an account via API with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        self.client.post(reverse('add-account'), data, format='json')
        query_params = {'employee': user.id}
        url_with_query_params = reverse('view-account') + '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])
        response = self.client.get(url_with_query_params, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_view_api_with_incorrect_data(self):
        """
        Test viewing an account via API with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        self.client.post(reverse('add-account'), data, format='json')
        query_params = {'employee': user.id - 10}
        url_with_query_params = reverse('view-account') + '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])
        response = self.client.get(url_with_query_params, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_account_update_api_with_correct_data(self):
        """
        Test updating an account via API with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        response = self.client.post(reverse('add-account'), data, format='json')
        url = reverse('update-account', kwargs={'pk': response.data['id']})
        data['salary'] = "25000"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_update_api_with_incorrect_data(self):
        """
        Test updating an account via API with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        response = self.client.post(reverse('add-account'), data, format='json')
        url = reverse('update-account', kwargs={'pk': response.data['id'] - 10})
        data['salary'] = "25000"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_account_delete_api_with_correct_data(self):
        """
        Test deleting an account via API with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        response = self.client.post(reverse('add-account'), data, format='json')
        url = reverse('delete-account', kwargs={'pk': response.data['id']})
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_account_delete_api_with_incorrect_data(self):
        """
        Test deleting an account via API with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "month": 2,
            "year": 2023,
            "salary": "10000.00"
        }
        response = self.client.post(reverse('add-account'), data, format='json')
        url = reverse('delete-account', kwargs={'pk': response.data['id'] - 10})
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
