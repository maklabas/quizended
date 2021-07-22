import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
# from app.forms import Form
from app.forms import QuestionForm
from app.models import Question

answer = 0
id_list = list(Question.objects.values_list('id', flat=True))
unique = list(range(len(id_list)))
random_id_1 = random.choice(unique)
unique.remove(random_id_1)
random_id_2 = random.choice(unique)
unique.remove(random_id_2)
random_id_3 = random.choice(unique)
unique.remove(random_id_3)

print('len ', len(id_list))
print(random_id_1)
print(random_id_2)
print(random_id_3)


class Form(forms.Form):
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
    global answer
    answer = 0

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
        context = {'form': form}
    return render(request, 'check.html', context=context)


def start(request):
    var = request.user.is_superuser
    print(var)
    return render(request, 'start.html')


def results(request):
    global answer
    if answer >= 2:
        message = 'Congratulations! You passed the quiz!'
    else:
        message = 'You failed the quiz. You can try again.'
    context = {'answer': answer,
               'message': message}
    return render(request, 'results.html', context=context)


def create_question(request):
    # If user == superuser

    if request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            # Check answers rigth or not
            question = form.save(commit=False)
            question.save()
        return redirect('check')

    form = QuestionForm()
    return render(request, 'create_question.html', {'form': form})
