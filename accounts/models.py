from django.db import models
from users.models import CustomUser

class Accounts(models.Model):
    """
    Model representing employee accounts.

    Attributes:
        employee (CustomUser): The employee associated with the accounts record (ForeignKey).
        month (int): The month of the accounts record.
        year (int): The year of the accounts record.
        salary (Decimal): The salary associated with the accounts record.

    Methods:
        __str__(): Returns a string representation of the accounts record.

    Meta:
        app_label (str): Specifies the app label for the accounts model (used for Django app configuration).
    """

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
        Returns a string representation of the accounts record.

        Returns:
            str: A formatted string with the employee's username, month, year, and salary.
        """
        return f"{self.employee.username} - {self.month}/{self.year} - Salary: {self.salary}"
    
    class Meta:
        """
        Meta class for Accounts.

        Attributes:
            app_label (str): Specifies the app label for the accounts model.
        """
        app_label = 'accounts'
