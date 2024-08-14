import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

with open('bot_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

questions = list(data.keys())
answers = list(data.values())

vectorizer = TfidfVectorizer().fit(questions)
question_vectors = vectorizer.transform(questions)

def get_reply(user_input):
    user_input_vector = vectorizer.transform([user_input])
    
    similarities = cosine_similarity(user_input_vector, question_vectors)
    
    best_match_index = np.argmax(similarities)
    
    if similarities[0, best_match_index] > 0.3:
        return answers[best_match_index]
    else:
        return "Tôi không hiểu bạn đang nói gì, bạn thử hỏi lại xem?"
