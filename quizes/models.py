from django.db import models
import random
# Create your models here.
DIFF_CHOICES = (
    ('Hiểu biết', 'Hiểu biết'),
    ('Vận dụng', 'Vận dụng'),
    ('Vận dụng cao', 'Vận dụng cao')
)
class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length = 120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="thời lượng")
    required_score_to_pass = models.IntegerField(help_text="điểm cần để qua")
    difficulty = models.CharField(max_length=20, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'
