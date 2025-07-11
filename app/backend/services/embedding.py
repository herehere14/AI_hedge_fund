from typing import List
import os


def embed_texts(texts: List[str], provider: str | None = None) -> List[List[float]]:
    """Generate embeddings using OpenAI or MiniLM."""
    provider = provider or os.getenv("EMBED_PROVIDER", "minilm")
    if provider.lower() == "openai":
        import openai
        resp = openai.embeddings.create(input=texts, model="text-embedding-3-small")
        return [d.embedding for d in resp.data]
    else:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return [vec.tolist() for vec in model.encode(texts)]


def embed_query(text: str) -> List[float]:
    return embed_texts([text])[0]
