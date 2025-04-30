from django.shortcuts import render, redirect
import uuid
from datetime import datetime

def save_quiz_result_to_session(request, quiz_name, score, answers):
    result_id = str(uuid.uuid4())
    result_data = {
        'id': result_id,
        'quiz_name': quiz_name,
        'score': score,
        'answers': answers,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    history = request.session.get('quiz_history', [])
    history.insert(0, result_data)
    request.session['quiz_history'] = history

    return result_id


def history_view(request):
    request.session.modified = True
    history = request.session.get('quiz_history', [])
    return render(request, 'results/history.html', {'results': history})


def result_detail_view(request, result_id):
    history = request.session.get('quiz_history', [])
    result = next((item for item in history if item['id'] == result_id), None)
    if not result:
        return render(request, 'results/not_found.html')

    return render(request, 'results/result_detail.html', {'result': result})
