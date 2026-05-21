from sqlalchemy import Column, Integer, String
from app.database.postgresql import Base, engine

from sqlalchemy import DateTime
from datetime import datetime
 
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_response = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)