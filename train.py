import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load the customer chat conversation dataset
df = pd.read_csv('customer_chat_conversations.csv')

# Split the dataset into features and labels
X = df['message_text']
y = df['intent']

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Transform the features into TF-IDF vectors
X_tfidf = vectorizer.fit_transform(X)

# Create a logistic regression classifier
clf = LogisticRegression()

# Train the classifier
clf.fit(X_tfidf, y)

# Create a function to predict the intent of a new customer message
def predict_intent(message):
  """Predicts the intent of a new customer message.

  Args:
    message: A string containing the customer message.

  Returns:
    A string containing the predicted intent.
  """

  # Transform the message into a TF-IDF vector
  message_tfidf = vectorizer.transform([message])

  # Make a prediction
  prediction = clf.predict(message_tfidf)

  # Return the predicted intent
  return prediction[0]

# Example usage:

message = "I'm having trouble logging into my account."

# Predict the intent of the message
intent = predict_intent(message)

# Print the predicted intent
print(intent)
