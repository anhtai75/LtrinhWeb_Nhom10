from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User

# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    
    def __str__(self):
        return str(self.pk)

class AnswerDetail(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='answer_details')
    question_text = models.CharField(max_length=1000)
    user_answer = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    @property
    def is_correct(self):
        return self.user_answer == self.correct_answer
