# OfficeAccountsAttendanceApp
Office Attendance and Accounts Management System

# Project Name

 A Django-based backend application for managing attendance and accounts in an office environment

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)

## Introduction

A Django backend application for employee attendance and accounts managment.

It has 3 apps as follows:
1. users (contains a model extended from django user model)
2. attendance (contains a model to record attendance of employees)
3. accounts   (cotains salary information of employees)

JWT authentication has been also incorporated in this app for API security. 
Morever, Django Rest Framework has been activated to make CRUD APIs for each of the three models using django models and serialisers. MongoDB is used as the database. 


## Features

1. app is capable of holding employee data.
2. app can keep track of employee attendance.
3. app can keep track of employee salary wrt month/year.

## Installation & setup instructions

0. clone the repo and navigate to proj dir.
1. run this command pip install -r requirements.txt
2. create a mongodb database named "employeeManagment" 
3. run commands for db migrations in django.
4. test crud apis with postman after creating a superuser and pass the creds with token calls
   to test the crud apis for each model 
