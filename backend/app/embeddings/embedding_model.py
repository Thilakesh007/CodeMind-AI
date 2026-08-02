from sentence_transformers import SentenceTransformer

model = None

def generate_embeddings(texts):
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings.tolist()