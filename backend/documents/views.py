# backend/documents/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Document
from analysis.services.document_analyzer import DocumentAnalyzer
import magic
import os

class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        if value.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(f'File too large. Max size: {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB')
        return value

class DocumentUploadView(APIView):
    """Handle document uploads"""
    
    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = serializer.validated_data['file']
        
        # Detect file type
        mime = magic.from_buffer(uploaded_file.read(1024), mime=True)
        uploaded_file.seek(0)
        
        # Determine document type
        if mime == 'application/pdf':
            doc_type = 'pdf'
        elif mime.startswith('image/'):
            doc_type = 'image'
        elif 'document' in mime:
            doc_type = 'document'
        elif 'spreadsheet' in mime or 'excel' in mime:
            doc_type = 'spreadsheet'
        elif mime == 'text/plain':
            doc_type = 'text'
        else:
            doc_type = 'other'
        
        # Save file
        file_path = default_storage.save(
            f'documents/{uploaded_file.name}',
            ContentFile(uploaded_file.read())
        )
        
        # Create document record
        document = Document.objects.create(
            file=file_path,
            original_name=uploaded_file.name,
            file_size=uploaded_file.size,
            file_type=doc_type,
            mime_type=mime,
            status='processing'
        )
        
        try:
            # Perform analysis
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            analysis_result = DocumentAnalyzer.analyze(
                full_path, 
                uploaded_file.name,
                mime
            )
            
            document.analysis_result = analysis_result
            document.status = 'completed'
            document.save()
            
            return Response({
                'id': document.id,
                'original_name': document.original_name,
                'file_size': document.file_size,
                'file_type': document.file_type,
                'mime_type': document.mime_type,
                'status': document.status,
                'analysis': analysis_result,
                'uploaded_at': document.uploaded_at,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            document.status = 'failed'
            document.error_message = str(e)
            document.save()
            return Response({
                'error': f'Analysis failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentListView(APIView):
    """List all documents"""
    
    def get(self, request):
        documents = Document.objects.all()[:50]  # Last 50
        data = [{
            'id': doc.id,
            'original_name': doc.original_name,
            'file_size': doc.file_size,
            'file_type': doc.file_type,
            'status': doc.status,
            'uploaded_at': doc.uploaded_at,
        } for doc in documents]
        return Response(data)

class DocumentDetailView(APIView):
    """Get document details"""
    
    def get(self, request, document_id):
        try:
            doc = Document.objects.get(id=document_id)
            return Response({
                'id': doc.id,
                'original_name': doc.original_name,
                'file_size': doc.file_size,
                'file_type': doc.file_type,
                'mime_type': doc.mime_type,
                'status': doc.status,
                'analysis': doc.analysis_result,
                'uploaded_at': doc.uploaded_at,
                'error_message': doc.error_message,
            })
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)