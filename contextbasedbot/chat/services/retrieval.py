from django.conf import settings
from pgvector.django import CosineDistance
from chat.models import DocumentChunk
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_similar_chunks(query, top_k=5, document_id=None):
    query_embedding = model.encode(query).tolist()
    results = (
        DocumentChunk.objects
        .filter(document_id=document_id)
        .annotate(similarity=CosineDistance("embedding", query_embedding))
        .filter(similarity__lte=settings.SIMILARITY_THRESHOLD)
        .order_by("similarity")[:top_k]
    )
    return results if results.exists() else []

def get_context_from_results(results):
    return " ".join([res.context for res in results])
