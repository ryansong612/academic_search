from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import gensim.downloader as api

def preprocess_text(text):
    # Tokenize the text into individual words
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Reconstruct the preprocessed text
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def rank_paragraphs(query, paragraphs):
    id = list(range(len(paragraphs) + 1))

    # Preprocess the query
    preprocessed_query = preprocess_text(query)
    
    # Preprocess the paragraphs
    preprocessed_paragraphs = [preprocess_text(p) for p in paragraphs]
    
    # Load pre-trained word embeddings (word2vec)
    word_embeddings = api.load('word2vec-google-news-300')
    
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the preprocessed paragraphs
    tfidf_matrix = vectorizer.fit_transform(preprocessed_paragraphs)
    
    # Transform the preprocessed query
    query_vector = vectorizer.transform([preprocessed_query])
    
    # Calculate the cosine similarity between the query and paragraphs using TF-IDF
    tfidf_similarity_scores = cosine_similarity(tfidf_matrix, query_vector).flatten()
    
    # Calculate the cosine similarity between the query and paragraphs using word embeddings
    query_embedding = np.mean([word_embeddings[word] for word in preprocessed_query.split() if word in word_embeddings], axis=0)
    paragraph_embeddings = [np.mean([word_embeddings[word] for word in paragraph.split() if word in word_embeddings], axis=0)
                            for paragraph in preprocessed_paragraphs]
    embedding_similarity_scores = cosine_similarity(paragraph_embeddings, [query_embedding]).flatten()
    
    # Combine the similarity scores from TF-IDF and word embeddings
    combined_similarity_scores = 0.6 * tfidf_similarity_scores + 0.4 * embedding_similarity_scores
    
    # Sort the paragraphs by the combined similarity score in descending order
    # ranked_paragraphs = sorted(zip(combined_similarity_scores, paragraphs, id), reverse=True)
    
    return combined_similarity_scores, paragraphs, id

# # Example usage
# query = "python programming"
# paragraphs = [
#     "Python is a widely used high-level programming language.",
#     "Java is another popular programming language.",
#     "Python has a simple syntax and is easy to learn.",
#     "Python is often used for web development and data analysis.",
#     "JavaScript is commonly used for front-end web development."
# ]

# combined_similarity_scores, paragraphs, id = rank_paragraphs(query, paragraphs)

# # print("Ranking of paragraphs by relevance to the query:")
# # for i, (score, paragraph, id) in enumerate(results):
# #     print(f"#{i+1}: {paragraph} (Score: {score:.2f})")

# print(combined_similarity_scores, paragraphs, id)
