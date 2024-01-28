from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model representing additional user information.

    Attributes:
        department (str): The department to which the user belongs.
        position (str): The position or role of the user.
        manager (CustomUser): The manager of the user, represented as a ForeignKey to self.
        date_of_birth (Date): The date of birth of the user.
        address (str): The address of the user.
        phone_number (str): The phone number of the user.
        emergency_contact_info (str, optional): Emergency contact information for the user.
        joining_date (Date): The date when the user joined the organization.
        termination_date (Date, optional): The date when the user was terminated (if applicable).
        skills_expertise (str, optional): Any skills or expertise the user possesses.

    Methods:
        __str__(): Returns a string representation of the user, using the username.

    Meta:
        app_label (str): Specifies the app label for the user model (used for Django app configuration).
    """

    department = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    date_of_birth = models.DateField(default='1985-03-15')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    emergency_contact_info = models.TextField(blank=True)
    joining_date = models.DateField(default='2005-03-15')
    termination_date = models.DateField(blank=True, null=True)
    skills_expertise = models.TextField(blank=True)

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username
    
    class Meta:
        """
        Meta class for CustomUser.

        Attributes:
            app_label (str): Specifies the app label for the user model (used for Django app configuration).
        """
        app_label = 'users'
