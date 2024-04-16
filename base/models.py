from django.db import models
import os
import uuid

class UploadedPDF(models.Model):
    pdf_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=200)
    PDF_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.PDF_file:
            os.remove(self.PDF_file.path)
        super(UploadedPDF, self).delete(*args, **kwargs)

class Chunk(models.Model):
    pdf = models.ForeignKey(UploadedPDF, on_delete=models.CASCADE)
    content = models.TextField()