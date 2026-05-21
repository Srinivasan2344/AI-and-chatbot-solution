from fastapi import FastAPI
from pydantic import BaseModel
import spacy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------- FASTAPI --------------------

app = FastAPI()

# -------------------- SPACY NLP --------------------

nlp = spacy.load("en_core_web_sm")

# -------------------- POSTGRESQL --------------------

DATABASE_URL = "postgresql://postgres:durai123@localhost/chatbot_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# -------------------- DATABASE MODEL --------------------

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_response = Column(String)
    intent = Column(String)

# Create Table
Base.metadata.create_all(bind=engine)

# -------------------- REQUEST MODEL --------------------

class UserMessage(BaseModel):
    message: str

# -------------------- CHATBOT RESPONSES --------------------

responses = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi! Welcome!",
    "bye": "Goodbye! Have a great day.",
    "what is artificial intelligence": "Artificial Intelligence is the simulation of human intelligence by machines.",
    "apple launched iphone in india": "Apple has launched iPhone in India."
}

# -------------------- CHAT API --------------------

@app.post("/chat")
def chat(user: UserMessage):

    try:

        db = SessionLocal()

        message = user.message.lower()

        # -------------------- INTENT RECOGNITION --------------------

        if "hello" in message or "hi" in message:
            intent = "greeting"

        elif "bye" in message:
            intent = "goodbye"

        else:
            intent = "general"

        # -------------------- ENTITY EXTRACTION --------------------

        doc = nlp(user.message)

        entities = []

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        # -------------------- BOT RESPONSE --------------------

        bot_response = responses.get(
            message,
            "Sorry, I don't understand your question."
        )

        # -------------------- SAVE TO DATABASE --------------------

        new_chat = ChatHistory(
            user_message=user.message,
            bot_response=bot_response,
            intent=intent
        )

        db.add(new_chat)
        db.commit()

        # -------------------- RESPONSE --------------------

        return {
            "user_message": user.message,
            "intent": intent,
            "entities": entities,
            "bot_response": bot_response
        }

    except Exception as e:

        return {
            "error": str(e)
        }