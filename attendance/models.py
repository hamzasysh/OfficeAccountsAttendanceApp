from django.db import models
from users.models import CustomUser

class Attendance(models.Model):
    """
    Model representing employee attendance.

    Attributes:
        employee (CustomUser): The employee associated with the attendance record (ForeignKey).
        check_in_time (DateTime): The time when the employee checked in.
        check_out_time (DateTime, optional): The time when the employee checked out (nullable).
        date (Date): The date of the attendance record.

    Methods:
        __str__(): Returns a string representation of the attendance record.

    Meta:
        app_label (str): Specifies the app label for the attendance model (used for Django app configuration).
    """

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        """
        Returns a string representation of the attendance record.

        Returns:
            str: A formatted string with the employee's username and the date.
        """
        return f"{self.employee.username} - {self.date}"
    
    class Meta:
        """
        Meta class for Attendance.

        Attributes:
            app_label (str): Specifies the app label for the attendance model.
        """
        app_label = 'attendance'
