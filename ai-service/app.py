from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

app = Flask(__name__)

DOMAIN_KEYWORDS = {
    "technology": ["ai", "machine learning", "deep learning", "data science", "python"],
    "sports": ["sport", "football", "basketball", "tennis", "training"],
}

@app.route('/match', methods=['POST'])
def match_users():
    data = request.json
    current_user = data['current_user']
    all_users = data['all_users']
    
    current_domain = detect_domain(current_user['interests'])
    
    domain_users = [
        user for user in all_users 
        if detect_domain(user['interests']) == current_domain
    ]
    
    if not domain_users:
        return jsonify([])
    
    documents = [' '.join(current_user['interests']).lower()]
    documents += [' '.join(user['interests']).lower() for user in domain_users]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    top_indices = cosine_sim.argsort()[0][-3:][::-1]
    
    return jsonify([domain_users[i] for i in top_indices])

def detect_domain(interests):
    """Strict domain detection using exact keyword matches"""
    domain_scores = defaultdict(int)
    
    for interest in interests:
        interest_lower = interest.lower()
        for domain, keywords in DOMAIN_KEYWORDS.items():
            if interest_lower in keywords:
                domain_scores[domain] += 1
                
    if not domain_scores:
        return "other"
        
    return max(domain_scores, key=domain_scores.get)

if __name__ == '__main__':
    app.run(port=5000, debug=True)