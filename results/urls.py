from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('history/', views.history_view, name='history'),
    path('history/<str:result_id>/', views.result_detail_view, name='result_detail'),
]

