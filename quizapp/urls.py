from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('landing/', views.landing_page, name='landing'),
    path('quiz/<int:quiz_id>/', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/<int:quiz_id>/home/', views.quiz_home, name='quiz_home'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('logout/', views.logout_view, name='logout')

]
