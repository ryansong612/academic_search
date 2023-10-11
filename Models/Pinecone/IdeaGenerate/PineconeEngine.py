import pinecone

pinecone.init(api_key="4b5aa89d-b17e-4337-a232-28f77bde92ab", environment="us-west4-gcp-free")
pinecone_index = pinecone.Index("stars-default")



import tensorflow_hub as hub
import tensorflow as tf
import numpy as np

# Load the Universal Sentence Encoder module
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
EmbeddingModel = hub.load(module_url)

def Vector(msg):
    eager_tensor = EmbeddingModel([msg])
    tensor_as_numpy = eager_tensor.numpy()
    tensor_as_list = tensor_as_numpy.tolist()
    return tensor_as_list


def PineconeSearchRequest(vector, k=10, namespace="chemistry_journals"):
    results = pinecone_index.query(
        vector=vector,
        top_k=k,
        namespace=namespace ,
        includeMetadata=True
    )
    return results

def PineconeSearch(msg, k=10):
    vector = Vector(msg)
    results = PineconeSearchRequest(vector, k)
    return results


PineconeSearch("polymer design")