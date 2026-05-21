from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from app.chatbot.intents import training_sentences, training_labels

# Convert text to numbers
vectorizer = CountVectorizer()

X = vectorizer.fit_transform(training_sentences)

# Train model
model = MultinomialNB()

model.fit(X, training_labels)

def predict_intent(text):

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)

    return prediction[0]