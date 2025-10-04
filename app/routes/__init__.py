from flask import Blueprint


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
game_bp = Blueprint("game", __name__, url_prefix="/game")
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def register_blueprints(app):
    from . import auth, game, admin 

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(admin_bp)
