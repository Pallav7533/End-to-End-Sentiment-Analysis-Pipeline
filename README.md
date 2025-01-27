# End-to-End Sentiment Analysis Pipeline

## **Objective**

This project implements a sentiment analysis pipeline using the IMDB movie review dataset. The pipeline covers data acquisition, preprocessing, training, model evaluation, and deployment of the trained model through a Flask API.

---

## **Project Setup**

### **1. Install Dependencies**
To install the required dependencies, create a virtual environment and use `pip` to install the packages listed in `requirements.txt`.

# Install the dependencies
pip install -r requirements.txt

### **2. Set Up PostgreSQL Database**

#1.install the postgresql
To set up PostgreSQL for the project, follow these steps:
On Windows: Download from https://www.postgresql.org/download/

#2. Create Database and Table:
CREATE DATABASE imdb_reviews_db;

#3. Database Connection

import psycopg2

conn = psycopg2.connect(
    dbname="imdb_reviews_db", 
    user="your_user", 
    password="your_password", 
    host="localhost", 
    port="5432"
)
cursor = conn.cursor()






