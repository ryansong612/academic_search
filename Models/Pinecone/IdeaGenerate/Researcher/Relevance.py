import tensorflow_hub as hub
import numpy as np
# Load the Universal Sentence Encoder module
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

def embed_sentences(sentences):
    # Generate embeddings for the sentences
    embeddings = model(sentences)
    return embeddings

def compute_similarity(embedding1, embedding2):
    # Compute cosine similarity between two embeddings
    similarity = np.inner(embedding1, embedding2)
    return similarity

def ParagraphsRank(query, paragraphs):
    # Embed the query and paragraphs
    itemsList = [query] + [paragraph['content'] for paragraph in paragraphs]
    embeddingList = embed_sentences(itemsList)
    
    query_embedding = embeddingList[0]
    paragraph_embeddings = embeddingList[1:]

    # Compute similarity scores between query and paragraphs
    similarity_scores = [compute_similarity(query_embedding, embedding) for embedding in paragraph_embeddings]

    # Add similarity scores to each paragraph dictionary
    for i, score in enumerate(similarity_scores):
        paragraphs[i]['score'] = float(score)

    # Sort paragraphs based on similarity scores
    ranked_paragraphs = sorted(paragraphs, key=lambda x: x['score'], reverse=True)

    return ranked_paragraphs