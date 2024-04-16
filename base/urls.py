from django.urls import path
from . import views

app_nbame='base'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.pdf_upload, name='pdf_upload'),
    path('pdfs/', views.pdf_list, name='pdf_list'),
    path('pdfs/<int:pdf_id>/', views.pdf_detail, name='pdf_detail'),
    path('pdfs/<int:pdf_id>/delete/', views.pdf_delete, name='pdf_delete'),
    path('pdfs/<int:pdf_id>/download/', views.pdf_download, name='download_pdf'),
    path('pdf/<int:pdf_id>/chunk/<int:chunk_index>/', views.chunk_detail, name='chunk_detail'),
    path('search/', views.search_results, name='search_results'),
]
