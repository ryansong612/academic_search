'''
This is a package that gives user direct access to popular functions.
'''

import tensorflow_hub as hub
import tensorflow as tf
import numpy as np


def embed_sentences(sentences):
    # Load the Universal Sentence Encoder module
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    # Generate embeddings for the sentences
    embeddings = model(sentences)
    return embeddings


def similarity(embedding1, embedding2):
    # Compute cosine similarity between two embeddings
    sim = np.inner(embedding1, embedding2)
    return sim
