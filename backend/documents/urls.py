# backend/documents/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.DocumentUploadView.as_view(), name='upload'),
    path('list/', views.DocumentListView.as_view(), name='list'),
    path('<uuid:document_id>/', views.DocumentDetailView.as_view(), name='detail'),
]