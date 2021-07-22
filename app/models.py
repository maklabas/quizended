from django.db import models

ANSWER_QUESTION_CHOICES = ((True, 'True'), (False, 'False'))


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=250, null=False, blank=False, verbose_name='Question Text')
    right_answer = models.BooleanField(choices=ANSWER_QUESTION_CHOICES, null=False, blank=False,
                                       verbose_name='Right answer on question')

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question_text
