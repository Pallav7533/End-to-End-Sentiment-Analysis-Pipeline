# End-to-End Sentiment Analysis Pipeline

## **Objective**

This project implements an end-to-end sentiment analysis pipeline using the IMDB movie review dataset. The pipeline covers data acquisition, preprocessing, model training, evaluation, and deployment through a Flask API.

---

## **Project Setup**

### **1. Install Dependencies**

To install the required dependencies, create a virtual environment and use `pip` to install the packages listed in `requirements.txt`.

```bash
# Create a virtual environment (optional)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

### **2. Set Up PostgreSQL Database**

To set up PostgreSQL for this project, follow these steps:

#### 1. **Install PostgreSQL:**

- On Ubuntu: `sudo apt install postgresql postgresql-contrib`
- On macOS: `brew install postgresql`
- On Windows: Download from [here](https://www.postgresql.org/download/).

#### 2. **Create Database and Table:**

1. Start PostgreSQL:
    ```bash
    sudo service postgresql start  # Linux
    brew services start postgresql  # macOS
    ```

2. Access PostgreSQL:
    ```bash
    sudo -u postgres psql  # Linux
    psql postgres  # macOS or Windows
    ```

3. Create a new database:
    ```sql
    CREATE DATABASE imdb_reviews_db;
    ```

4. Switch to the new database:
    ```sql
    \c imdb_reviews_db;
    ```

5. Create a table for the reviews:
    ```sql
    CREATE TABLE imdb_reviews (
        id SERIAL PRIMARY KEY,
        review_text TEXT NOT NULL,
        sentiment VARCHAR(10) NOT NULL
    );
    ```

#### 3. **Database Connection:**

In your `app.py` file, replace the SQLite connection with a PostgreSQL connection:

```python
import psycopg2

conn = psycopg2.connect(
    dbname="imdb_reviews_db", 
    user="your_user", 
    password="your_password", 
    host="localhost", 
    port="5432"
)
cursor = conn.cursor()
```

---

## **Data Acquisition**

The dataset used in this project is the IMDB Movie Reviews dataset. It is publicly available and can be loaded using Hugging Face's `datasets` library.

1. **Loading the Data:**

```python
from datasets import load_dataset
dataset = load_dataset("imdb")
```

2. **Database Insertion:**

The dataset is processed and inserted into PostgreSQL using the following code:

```python
import psycopg2
from datasets import load_dataset

dataset = load_dataset("imdb")
conn = psycopg2.connect(
    dbname="imdb_reviews_db", 
    user="your_user", 
    password="your_password", 
    host="localhost", 
    port="5432"
)
cursor = conn.cursor()

# Insert data into the database
for review, sentiment in zip(dataset['train']['text'], dataset['train']['label']):
    cursor.execute("INSERT INTO imdb_reviews (review_text, sentiment) VALUES (%s, %s)", (review, sentiment))

conn.commit()
conn.close()
```

---

## **Run Instructions**

### **1. Train the Model**

To train the model on the IMDB dataset, run the following Python script:

```bash
python train_model.py
```

This will:
- Preprocess the dataset (cleaning text, removing HTML tags, etc.).
- Train a logistic regression model using `TfidfVectorizer`.
- Save the trained model as `logistic_regression_model.pkl` and the vectorizer as `tfidf_vectorizer.pkl`.

### **2. Start the Flask Server**

To start the Flask server and serve the trained model, run:

```bash
python app.py
```

### **3. Test the Endpoint**

Once the server is running, you can test the `/predict` endpoint with the following methods:

#### **Using cURL**

```bash
curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d '{"review_text": "This movie was amazing!"}'
```

#### **Using Postman**

1. Open Postman and create a new `POST` request.
2. URL: `http://127.0.0.1:5000/predict`
3. Set the body to `raw` and `JSON` type:
   ```json
   {
     "review_text": "This movie was amazing!"
   }
   ```

#### **Using Python's Requests Library**

```python
import requests

url = "http://127.0.0.1:5000/predict"
data = {"review_text": "This movie was amazing!"}
response = requests.post(url, json=data)
print(response.json())
```

The expected output will be:

```json
{
  "sentiment_prediction": "positive"
}
```

---

## **Model Info**

### **Model Approach**
- **Model Type**: Logistic Regression
- **Features**: TF-IDF vectors
- **Training Dataset**: IMDB Movie Reviews dataset (25k labeled reviews)
- **Model Evaluation**:
  - **Accuracy**: 88%
  - **Precision**: 0.89 (positive), 0.87 (negative)
  - **Recall**: 0.87 (positive), 0.89 (negative)
  - **F1-Score**: 0.88 (positive), 0.88 (negative)

---

## **Future Enhancements**
- Experiment with transformer-based models like **BERT** or **DistilBERT** for improved accuracy.
- Deploy on a globally distributed platform (e.g., **AWS**, **Fly.io**).
- Add caching for faster predictions.

---

## **Contact**
- **Author**: Pallav Havda
- **Email**: [your-email@example.com](mailto:your-email@example.com)
