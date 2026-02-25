from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os
import json

# Use environment variable or default to app.db in the same directory
DATABASE_URL = os.environ.get("PREPSYNC_DATABASE_URL") or os.environ.get("DATABASE_URI") or f"sqlite:///{os.path.join(os.path.dirname(__file__), 'app.db')}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    history = relationship("History", back_populates="user", cascade="all, delete-orphan")

class History(Base):
    __tablename__ = 'history'
    id = Column(String(64), primary_key=True)
    user_email = Column(String(255), ForeignKey('users.email', ondelete="CASCADE"), index=True, nullable=False)
    slug = Column(String(255), nullable=False, default="")
    examName = Column(String(255), nullable=False, default="")
    pausedTopic = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="history")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()

def migrate_from_json(json_path: str | None = None):
    data_path = json_path or os.path.join(os.path.dirname(__file__), "data.json")
    if not os.path.exists(data_path):
        return
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    users_dict = data.get("users") or {}
    with SessionLocal() as db:
        for email, u in users_dict.items():
            existing = db.query(User).filter_by(email=email).first()
            if not existing:
                db.add(User(email=email, username=(u.get("username") or (email.split('@')[0])), password=(u.get("password") or "")))
            hist_list = u.get("history") or []
            for h in hist_list:
                if not db.get(History, h.get("id")):
                    db.add(History(
                        id=h.get("id"),
                        user_email=email,
                        slug=h.get("slug") or "",
                        examName=h.get("examName") or "",
                        pausedTopic=h.get("pausedTopic") or ""
                    ))
        for h in (data.get("history") or []):
            email = (data.get("profile") or {}).get("email") or "guest@example.com"
            if not db.query(User).filter_by(email=email).first():
                username = (data.get("profile") or {}).get("username") or "Guest"
                db.add(User(email=email, username=username, password=""))
            if not db.get(History, h.get("id")):
                db.add(History(
                    id=h.get("id"),
                    user_email=email,
                    slug=h.get("slug") or "",
                    examName=h.get("examName") or "",
                    pausedTopic=h.get("pausedTopic") or ""
                ))
        db.commit()
