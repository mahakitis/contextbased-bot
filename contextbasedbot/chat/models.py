from django.db import models
from pgvector.django import VectorField
import uuid
# Create your models here.
class Document(models.Model):
    doc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=255)    #to put if it is a pdf, youtube or website link
    added_at = models.DateTimeField(auto_now_add=True)
    
class DocumentChunk(models.Model):
    chunk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    context = models.TextField()
    embedding = VectorField(dimensions=384)
    
class ChatHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chat_history")
    question = models.TextField()
    answer = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)