# Generated by Django 4.1.13 on 2024-01-26 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(default='2005-03-15'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='joining_date',
            field=models.DateField(default='2005-03-15'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='position',
            field=models.CharField(max_length=50),
        ),
    ]
