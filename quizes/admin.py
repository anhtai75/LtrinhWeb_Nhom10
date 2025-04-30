from django.contrib import admin
from .models import Quiz

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'number_of_questions', 'time', 'required_score_to_pass', 'difficulty')
    list_filter = ('difficulty',)
    search_fields = ('name', 'topic')
    ordering = ('name',)
