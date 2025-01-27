from flask import Flask, render_template, request, jsonify
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize Flask app
app = Flask(__name__)

# Load the saved model and vectorizer
MODEL_PATH = 'logistic_regression_model.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    raise FileNotFoundError("Model or vectorizer file not found. Ensure both are saved in the current directory.")

# Home route for rendering HTML
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            review_text = request.form.get('review_text', '')

            if not review_text.strip():
                return render_template('index.html', error="Please enter a valid review.")

            review_tfidf = vectorizer.transform([review_text])

            # Predict sentiment
            prediction = model.predict(review_tfidf)[0]  # 1 = Positive, 0 = Negative

            # Map sentiment label
            sentiment = 'Positive' if prediction == 1 else 'Negative'
            
            return render_template('index.html', prediction=sentiment)

        except Exception as e:
            return render_template('index.html', error="An error occurred during prediction. Please try again.")

    # Render the initial form
    return render_template('index.html')

#API for prediction
@app.route('/predict', methods=['POST'])
def predict_sentiment():
    try:
        if request.is_json:
            data = request.get_json()
            review_text = data.get('review_text', '')
        else:
            review_text = request.form.get('review_text', '')

        if not review_text.strip():
            return jsonify({'error': "Please provide a valid review."}), 400

        review_tfidf = vectorizer.transform([review_text])

        prediction = model.predict(review_tfidf)[0]  # 1 = Positive, 0 = Negative

        sentiment = 'positive' if prediction == 1 else 'negative'
        
        return jsonify({'sentiment_prediction': sentiment}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
