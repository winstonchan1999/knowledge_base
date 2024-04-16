from django.contrib import admin
from .models import UploadedPDF, Chunk

admin.site.register(UploadedPDF)
admin.site.register(Chunk)