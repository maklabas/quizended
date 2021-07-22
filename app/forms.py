from django import forms
from django.forms import ModelForm

# from app.views import id_list, random_id_1, random_id_2, random_id_3
from app import views
from app.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'right_answer']
        widgets = {
            'question_text': forms.Textarea(attrs={'placeholder': 'Your question text'})
        }

# class Form(forms.Form):
#     CHOICES = [(True, True), (False, False)]
#     label1 = Question.objects.get(id=id_list[random_id_1]).question_text
#     choice_field1 = forms.ChoiceField(label=label1, widget=forms.RadioSelect, choices=CHOICES)
#     label2 = Question.objects.get(id=id_list[random_id_2]).question_text
#     choice_field2 = forms.ChoiceField(label=label2, widget=forms.RadioSelect, choices=CHOICES)
#     label3 = Question.objects.get(id=id_list[random_id_3]).question_text
#     choice_field3 = forms.ChoiceField(label=label3, widget=forms.RadioSelect, choices=CHOICES)
