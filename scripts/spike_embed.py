import sys
import time
from pathlib import Path
import os

# Add root directory to sys.path to allow importing shop_assistant
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

import numpy as np
from ollama import Client

from shop_assistant import config
from shop_assistant.textnorm import normalise
def main():
    ollama_url = getattr(config, "OLLAMA_URL", "http://192.168.0.218:11434")
    embed_model = getattr(config, "EMBED_MODEL", "bge-m3")

    print(f"Using Ollama URL: {ollama_url}")
    print(f"Using Embed Model: {embed_model}")

    client = Client(host=ollama_url)
    
    words = [
        "krossovka",
        "кроссовки",
        "sneakers",
        "kurtka",
        "куртка",
        "jacket",
        "dvoyka",
        "телефон"
    ]
    
    print(f"Embedding {len(words)} words (after normalisation)...")
    
    start_time = time.time()
    
    try:
        normalised_words = [normalise(w) for w in words]
        result = client.embed(model=embed_model, input=normalised_words)
    except Exception as e:
        print(f"Error calling Ollama API: {e}")
        return
        
    wall_time = time.time() - start_time
    
    embeddings = result.get('embeddings', [])
    if not embeddings:
        print("No embeddings returned!")
        return
        
    vecs = np.array(embeddings)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    vecs_normalized = vecs / norms
    
    similarity_matrix = np.dot(vecs_normalized, vecs_normalized.T)
    dim = vecs.shape[1]
    
    print(f"\nEmbedding dimension: {dim}")
    print(f"Wall time: {wall_time:.3f} seconds")
    
    print("\nCosine Similarity Matrix:")
    header = "          " + "".join([f"{w[:7]:>10}" for w in words])
    print(header)
    
    for i, row_word in enumerate(words):
        row_str = f"{row_word[:9]:>10}"
        for j in range(len(words)):
            row_str += f"{similarity_matrix[i, j]:10.3f}"
        print(row_str)

if __name__ == "__main__":
    main()
