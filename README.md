Quiz Management System

This project is a Quiz Management System built with Django. It allows users to register, log in, take quizzes, and view their results. Admin users have the ability to create and manage quizzes, questions, and answers via the Django admin panel. The system also tracks user attempts, scores, and provides functionality for attempting each quiz only once.

Key Features
----------------

1.User Authentication:

    User registration, login, and logout functionality.

    Password validation during registration.

2.Admin Interface:

    Admin can create, update, and delete quizzes, questions, options, and manage user attempts through Django’s built-in admin interface.

3.Quiz Flow:

    Users can browse available quizzes.

    Users can answer multiple-choice questions for each quiz.

    The system tracks each user’s progress through the quiz and only allows one attempt per quiz.

4.Score Tracking:

    After completing a quiz, users can view their score based on correct answers.

    The system keeps track of which questions have been answered.

Requirements
----------------

    Python 3.12

    Django 5.2

    Django REST Framework

    SQLite Database (used by default)

Installation
-----------------

    1.Create folder

    2.Set Up a Virtual Environment(python -m venv venv)

    3.Install Dependencies

        pip install django
        pip install djangorestframework

    4.Apply Database Migrations

    5.Create a Superuser (Admin Account)
        python manage.py createsuperuser

    6.Run the Development Server
        python manage.py runserver
    
The application will be available at http://127.0.0.1:8000/.


