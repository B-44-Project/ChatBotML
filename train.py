# https://chat.openai.com/share/ae0f6fb0-6797-471c-91fd-f541c3f4f803
# incomplete version
# train_chatbot.py

import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import json

# Load intents file
with open("data/intents.json") as file:
    data = json.load(file)

# Extract data for training
intents = data["intents"]
patterns = []
responses = []
tags = []

for intent in intents:
    for pattern in intent["patterns"]:
        patterns.append(pattern.lower())
        tags.append(intent["tag"])
    responses.extend(intent["responses"])

# Tokenize words
lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(word) for word in patterns if word.isalnum()]
words = sorted(set(words))

# Create training data
training_data = []
output_empty = [0] * len(tags)

for idx, pattern in enumerate(patterns):
    bag = []
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern.split() if word.isalnum()]
    
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[tags.index(tags[idx])] = 1

    training_data.append([bag, output_row])

# Shuffle the training data
np.random.shuffle(training_data)
training_data = np.array(training_data)

# Split data into input and output
train_x = list(training_data[:, 0])
train_y = list(training_data[:, 1])

# Build the model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# Train the model
model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Save the trained model
model.save("models/chatbot_model.pkl", model_format="h5")

print("Chatbot model trained successfully.")
