# backend/documents/models.py

from django.db import models
import uuid

class Document(models.Model):
    """Main document model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('document', 'Word Document'),
        ('spreadsheet', 'Spreadsheet'),
        ('text', 'Text File'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    original_name = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    mime_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Analysis results
    analysis_result = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.original_name} - {self.uploaded_at}"
    
    @property
    def size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)