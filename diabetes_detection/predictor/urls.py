# predictor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('result/<int:patient_id>/', views.result, name='result'),
    path('history/', views.history, name='history'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
]
