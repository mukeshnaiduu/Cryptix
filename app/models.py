from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .extensions import db, bcrypt, login_manager


class Roles:
    PLAYER = "player"
    ADMIN = "admin"


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Roles.PLAYER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    games = relationship("Game", back_populates="player", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == Roles.ADMIN


class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(5), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    games = relationship("Game", back_populates="word", lazy="dynamic")


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    won = db.Column(db.Boolean)

    player = relationship("User", back_populates="games")
    word = relationship("Word", back_populates="games")
    guesses = relationship("Guess", back_populates="game", cascade="all, delete-orphan", lazy="dynamic")


class Guess(db.Model):
    __tablename__ = "guesses"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    attempt_number = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(5), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_correct = db.Column(db.Boolean, default=False)

    game = relationship("Game", back_populates="guesses")
