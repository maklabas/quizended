import random
from django.shortcuts import render, redirect
from django import forms
from app.forms import QuestionForm
from app.models import Question
from django.http import HttpResponse

# from app.forms import

# Переменная на валидацию суперпользователя. Проходит валидацию на стартовой странице
superuser_isvalid = False
random_id_1 = 0
random_id_2 = 0
random_id_3 = 0

# Подсчет правильных ответов. Обнуляется при повторном прохождении квиза
answer = 0
# список ид, которые есть в бд. По этим ид я беру случайные вопросы
id_list = list(Question.objects.values_list('id', flat=True))


def make_random_questions():
    # Список порядковых номеров ид.
    # По этим порядковым номерам я беру номер ид, чтобы вопросы не повторялись,
    # потом удаляю спользованный порядковый номер вопроса из списка. После этого тот же вопрос повторяться не будет
    unique = list(range(len(id_list)))
    global random_id_1, random_id_2, random_id_3
    random_id_1 = random.choice(unique)  # Выбираю случайный ид
    unique.remove(random_id_1)  # Далее его удаляю
    random_id_2 = random.choice(unique)
    unique.remove(random_id_2)
    random_id_3 = random.choice(unique)
    unique.remove(random_id_3)
    print(unique)
    print('len ', len(id_list))
    print(random_id_1)
    print(random_id_2)
    print(random_id_3)


make_random_questions()


class Form(forms.Form):
    """
     Форма квиза, которая должна быть в forms.py, но я текст вопроса поместил в label, что не совсем правильно.
    Из-за этого если переместить форму в forms.py, возникает:
    ImportError: cannot import name ... (most likely due to a circular import)
    """
    CHOICES = [(True, True), (False, False)]
    label1 = Question.objects.get(id=id_list[random_id_1]).question_text
    choice_field1 = forms.ChoiceField(label=label1, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}),
                                      choices=CHOICES)
    label2 = Question.objects.get(id=id_list[random_id_2]).question_text
    choice_field2 = forms.ChoiceField(label=label2, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}),
                                      choices=CHOICES)
    label3 = Question.objects.get(id=id_list[random_id_3]).question_text
    choice_field3 = forms.ChoiceField(label=label3, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}),
                                      choices=CHOICES)


def check(request):
    """ Представление квиза. После прохождения формы редиректит на results"""
    global answer
    answer = 0
    make_random_questions()

    if request.method == "POST":

        check_true1 = request.POST.get('choice_field1', 'no answer')
        check_true2 = request.POST.get('choice_field2', 'no answer')
        check_true3 = request.POST.get('choice_field3', 'no answer')

        if check_true1 == str(Question.objects.get(id=id_list[random_id_1]).right_answer):
            answer += 1
        if check_true2 == str(Question.objects.get(id=id_list[random_id_2]).right_answer):
            answer += 1
        if check_true3 == str(Question.objects.get(id=id_list[random_id_3]).right_answer):
            answer += 1

        return redirect('results')
    else:

        form = Form()
        context = {'form': form,
                   'superuser': superuser_isvalid}
    return render(request, 'app_templates/check.html', context=context)


def start(request):
    """Начальная страница с кнопкой. Здесь суперюзер проходит валидацию."""
    global superuser_isvalid
    superuser_isvalid = request.user.is_superuser
    return render(request, 'app_templates/start.html', {'superuser': superuser_isvalid})


def results(request):
    """Вывод количества правильных ответов и сообщения о прохождении теста"""
    global answer
    if answer >= 2:
        message = 'Congratulations! You passed the quiz!'
    else:
        message = 'You failed the quiz. You can try again.'
    context = {'answer': answer,
               'message': message,
               'superuser': superuser_isvalid}
    return render(request, 'app_templates/results.html', context=context)


def create_question(request):
    """ Создание вопроса. Доступ имеет только суперпользователь.
    Если ввести урл в адресной строке и суперпользователь не валидирован,
    представление редиректит на начальную страницу с валидацией."""
    if superuser_isvalid:
        if request.method == "POST":
            form = QuestionForm(data=request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.save()
            return redirect('start')

        form = QuestionForm()
        context = {'form': form,
                   'superuser': superuser_isvalid}
        return render(request, 'app_templates/create_question.html', context=context)
    else:
        return redirect('start')
