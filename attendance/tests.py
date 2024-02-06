from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.models import CustomUser
from attendance.models import Attendance
import uuid
from django.urls import reverse

class AttendanceTests(TestCase):
    """
    Test cases for the Attendance model and API views.
    """

    def setUp(self):
        """
        Set up common data for the test cases.
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

    def test_attendance_model_create_attendance(self):
        """
        Test creating an Attendance model instance.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        attendance = Attendance.objects.create(**data)
        self.assertEqual(attendance.employee, data['employee'])
        self.assertEqual(attendance.check_in_time, data['check_in_time'])
        self.assertEqual(attendance.check_out_time, data['check_out_time'])
        self.assertEqual(attendance.date, data['date'])

    def test_attendance_str_representation(self):
        """
        Test the string representation of the Attendance model.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        attendance = Attendance.objects.create(**data)
        self.assertEqual(str(attendance), f"{attendance.employee.username} - {attendance.date}")

    def test_attendance_create_api_with_correct_data(self):
        """
        Test the API endpoint to create Attendance with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        response = self.client.post(reverse('add-attendance'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_attendance_create_api_with_incorrect_data(self):
        """
        Test the API endpoint to create Attendance with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        response = self.client.post(reverse('add-attendance'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_attendance_view_api_with_correct_data(self):
        """
        Test the API endpoint to view Attendance with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        self.client.post(reverse('add-attendance'), data, format='json')
        query_params = {'employee': user.id}
        url_with_query_params = reverse('view-attendance') + '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])
        response = self.client.get(url_with_query_params, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attendance_view_api_with_incorrect_data(self):
        """
        Test the API endpoint to view Attendance with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        self.client.post(reverse('add-attendance'), data, format='json')
        query_params = {'employee': user.id - 10}
        url_with_query_params = reverse('view-attendance') + '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])
        response = self.client.get(url_with_query_params, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_attendance_update_api_with_correct_data(self):
        """
        Test the API endpoint to update Attendance with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        response = self.client.post(reverse('add-attendance'), data, format='json')
        url = reverse('update-attendance', kwargs={'pk': response.data['id']})
        data['date'] = "2024-01-23"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attendance_update_api_with_incorrect_data(self):
        """
        Test the API endpoint to update Attendance with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        response = self.client.post(reverse('add-attendance'), data, format='json')
        url = reverse('update-user', kwargs={'pk': response.data['id'] - 10})
        data['date'] = "2024-01-22"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_attendance_delete_api_with_correct_data(self):
        """
        Test the API endpoint to delete Attendance with correct data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        response = self.client.post(reverse('add-attendance'), data, format='json')
        url = reverse('delete-attendance', kwargs={'pk': response.data['id']})
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_attendance_delete_api_with_incorrect_data(self):
        """
        Test the API endpoint to delete Attendance with incorrect data.
        """
        user = CustomUser.objects.create(**self.user_data)
        data = {
            "employee": user.id,
            "check_in_time": "2024-01-29T15:33:15.160Z",
            "check_out_time": "2024-01-29T15:33:15.160Z",
            "date": "2024-01-29"
        }
        response = self.client.post(reverse('add-attendance'), data, format='json')
        url = reverse('delete-attendance', kwargs={'pk': response.data['id'] - 10})
        response = self.client.delete(url, None)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
