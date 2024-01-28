
from django.urls import path
from . import views
"""
URL patterns for the 'attendance' app.

Each URL pattern is associated with a specific view function from the 'views' module.

- '' (home): Display the API overview.
- 'create/': Add new attendance records.
- 'all/': View all attendance records.
- 'update/<int:pk>/': Update attendance records with a specific primary key.
- '<int:pk>/delete/': Delete attendance records with a specific primary key.
- 'hello/': Display a hello message.

Note:
- The 'name' parameter in each path is used to create named URLs, making it easier to reference them in templates or code.
- The '<int:pk>/' syntax is used to capture an integer primary key from the URL and pass it to the associated view function.

See Also:
- Django URL Patterns: https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""

urlpatterns = [
    
    path('', views.ApiOverview, name='home'),
    path('create/', views.add_attendance, name='add-users'),
    path('all/', views.view_attendance, name='view-users'),
    path('update/<int:pk>/', views.update_attendance, name='update_users'),
    path('<int:pk>/delete/', views.delete_attendance, name='delete-items'),
    path('hello/', views.hello_message, name='hello'),

]