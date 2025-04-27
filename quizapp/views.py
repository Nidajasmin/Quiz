from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Option, UserQuiz
from django.contrib import messages
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Username: {username}, Password: {password}")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def landing_page(request):
    quizzes = Quiz.objects.all()
    return render(request, 'landing.html', {'quizzes': quizzes})

@login_required
def quiz_home(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz.html', {'quiz': quiz, 'questions': questions})


@login_required
def question_detail(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id)
    options = Option.objects.filter(question=question)

    user_quiz, created = UserQuiz.objects.get_or_create(user=request.user, quiz=quiz)
    if user_quiz.attempted:
        messages.error(request, "Access Denied! You have already completed this quiz.")
        return redirect('landing')

   
    previous_question = Question.objects.filter(quiz=quiz, id__lt=question.id).order_by('-id').first()

    selected_option = user_quiz.selected_options.filter(question=question).first()

    if request.method == 'POST':
        selected_option_id = request.POST.get('selected_option')

        if selected_option_id:
            selected_option_obj = get_object_or_404(Option, id=selected_option_id)

            if not user_quiz.selected_options.filter(question=question).exists():
                user_quiz.selected_options.add(selected_option_obj)

                if selected_option_obj.is_correct:
                    user_quiz.score += 1
                user_quiz.answered_questions.add(question)
                user_quiz.save()

        all_questions = Question.objects.filter(quiz=quiz)
        answered_question_ids = user_quiz.answered_questions.values_list('id', flat=True)
        next_question = all_questions.exclude(id__in=answered_question_ids).first()

        if next_question:
            return redirect('question_detail', quiz_id=quiz.id, question_id=next_question.id)
        else:
            user_quiz.attempted = True
            user_quiz.save()
            return redirect('quiz_result', quiz_id=quiz.id)

    all_questions = Question.objects.filter(quiz=quiz)
    answered_question_ids = user_quiz.answered_questions.values_list('id', flat=True)
    remaining_questions = all_questions.exclude(id__in=answered_question_ids)
    is_last_question = (remaining_questions.count() == 1)  
    return render(request, 'question.html', {
        'quiz': quiz,
        'question': question,
        'options': options,
        'previous_question': previous_question,
        'total_questions': all_questions.count(),
        'answered_count': user_quiz.answered_questions.count(),
        'remaining_count': all_questions.count() - user_quiz.answered_questions.count(),
        'selected_option': selected_option,
        'is_last_question': is_last_question,
    })


@login_required
def attempt_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_attempted = UserQuiz.objects.filter(user=request.user, quiz=quiz).exists()

    if user_attempted:
        messages.error(request, "You have already attempted this quiz!")
        return redirect('landing')  

    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_quiz = get_object_or_404(UserQuiz, user=request.user, quiz=quiz)
    return render(request, 'result.html', {'quiz': quiz, 'score': user_quiz.score})
