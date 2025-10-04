from datetime import date

from flask import abort, render_template, request
from flask_login import current_user

from ..extensions import db
from ..models import Game, Roles, User, Word
from . import admin_bp


def _require_admin():
    if not current_user.is_authenticated or not current_user.is_admin():
        abort(403)


@admin_bp.before_request
def ensure_admin():
    _require_admin()


@admin_bp.route("/dashboard")
def dashboard():
    total_words = Word.query.count()
    total_players = User.query.filter_by(role=Roles.PLAYER).count()
    total_admins = User.query.filter_by(role=Roles.ADMIN).count()
    return render_template(
        "admin/dashboard.html",
        total_words=total_words,
        total_players=total_players,
        total_admins=total_admins,
    )


@admin_bp.route("/reports/daily")
def daily_report():
    report_date = request.args.get("date")
    if report_date:
        report_date = date.fromisoformat(report_date)
    else:
        report_date = date.today()

    query = Game.query.filter(db.func.date(Game.started_at) == report_date)
    users_played = query.with_entities(Game.player_id).distinct().count()
    wins = query.filter(Game.won.is_(True)).count()

    return render_template(
        "admin/daily_report.html",
        report_date=report_date,
        users_played=users_played,
        wins=wins,
    )


@admin_bp.route("/reports/user/<int:user_id>")
def user_report(user_id: int):
    player = User.query.get_or_404(user_id)
    if player.role != Roles.PLAYER:
        abort(404)

    stats = (
        db.session.query(
            db.func.date(Game.started_at).label("played_on"),
            db.func.count(Game.id).label("games_played"),
            db.func.sum(db.case((Game.won.is_(True), 1), else_=0)).label("wins"),
        )
        .filter(Game.player_id == player.id)
        .group_by(db.func.date(Game.started_at))
        .order_by(db.func.date(Game.started_at).desc())
        .all()
    )

    return render_template(
        "admin/user_report.html",
        player=player,
        stats=stats,
    )


@admin_bp.route("/players")
def players():
    players = User.query.filter_by(role=Roles.PLAYER).order_by(User.username.asc()).all()
    return render_template("admin/players.html", players=players)
