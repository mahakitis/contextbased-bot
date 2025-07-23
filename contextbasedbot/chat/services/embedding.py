from concurrent.futures import ThreadPoolExecutor, as_completed
from sentence_transformers import SentenceTransformer
from chat.models import DocumentChunk
from .chunking import read_and_chunk_text

model = SentenceTransformer("all-MiniLM-L6-v2")

MAX_WORKERS = 10

def embed_and_store(chunk, document):
    embedding = model.encode(chunk)
    DocumentChunk.objects.create(
        document=document,
        context=chunk,
        embedding=embedding.tolist()
    )

def embed_and_store_text(text, document):
    chunks = read_and_chunk_text(text)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(embed_and_store, chunk, document) for chunk in chunks]
        for future in as_completed(futures):
            future.result()  # raise exceptions if any
