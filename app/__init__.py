import os
from datetime import date
from pathlib import Path

from flask import Flask, render_template
from flask_login import current_user

from .extensions import bcrypt, db, login_manager, migrate
from .routes import register_blueprints
from .models import Game


def create_app(config_object: str | None = None) -> Flask:
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "change-this-secret"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///cryptix.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config_object:
        app.config.from_object(config_object)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    _register_extensions(app)
    register_blueprints(app)
    _register_routes(app)
    _register_cli(app)

    return app


def _register_extensions(app: Flask) -> None:
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"


def _register_routes(app: Flask) -> None:
    @app.route("/")
    def dashboard():  # type: ignore[misc]
        remaining_games = None
        recent_games = []

        if current_user.is_authenticated and not current_user.is_admin():
            today = date.today()
            played_today = (
                Game.query.filter(Game.player_id == current_user.id)
                .filter(db.func.date(Game.started_at) == today)
                .count()
            )
            remaining_games = max(0, 3 - played_today)
            recent_games = (
                Game.query.filter_by(player_id=current_user.id)
                .order_by(Game.started_at.desc())
                .limit(5)
                .all()
            )

        return render_template(
            "dashboard.html",
            remaining_games=remaining_games,
            recent_games=recent_games,
        )


def _register_cli(app: Flask) -> None:
    from .cli import init_cli

    init_cli(app)
