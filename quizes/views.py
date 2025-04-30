from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'

def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answer():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

def save_quiz_view(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken', None)

        questions = []
        for k in data_.keys():
            try:
                question = Question.objects.get(text=k)
                questions.append(question)
            except Question.DoesNotExist:
                continue

        quiz = Quiz.objects.get(pk=pk)

        score = 0
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(str(q.text))
            if a_selected:
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    elif a.correct:
                        correct_answer = a.text
                results.append({
                    'question': str(q),
                    'answered': a_selected,
                    'correct_answer': correct_answer,
                    'is_correct': a_selected == correct_answer
                })
            else:
                results.append({
                    'question': str(q),
                    'answered': None,
                    'correct_answer': None,
                    'is_correct': False
                })

        score_ = round((score / quiz.number_of_questions) * 10, 2)

        # Lưu vào session
        from results.views import save_quiz_result_to_session

        answers_for_session = [
            {
                'question_text': r['question'],
                'user_answer': r['answered'],
                'correct_answer': r['correct_answer']
            }
            for r in results
        ]

        save_quiz_result_to_session(request, quiz.name, score_, answers_for_session)
        request.session.modified = True

        return JsonResponse({
            'passed': score_ >= quiz.required_score_to_pass,
            'score': score_,
            'results': results
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
