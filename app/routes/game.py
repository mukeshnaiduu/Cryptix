from collections import Counter
from datetime import date, datetime
import random

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Game, Guess, Word
from . import game_bp


MAX_DAILY_GAMES = 3
MAX_ATTEMPTS = 5


def _today_game_count(user_id: int) -> int:
    today = date.today()
    return (
        Game.query.filter(Game.player_id == user_id)
        .filter(db.func.date(Game.started_at) == today)
        .count()
    )


def _choose_word() -> Word:
    words = Word.query.filter_by(active=True).all()
    return random.choice(words) if words else None


@game_bp.before_request
def ensure_authenticated():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if current_user.is_admin():
        flash("Admin accounts don't play the game. Use the admin dashboard instead.", "info")
        return redirect(url_for("admin.dashboard"))


@game_bp.route("/start")
def start():
    if _today_game_count(current_user.id) >= MAX_DAILY_GAMES:
        flash("Daily game limit reached. Come back tomorrow!", "warning")
        return redirect(url_for("dashboard"))

    word = _choose_word()
    if not word:
        flash("No words available. Please contact an administrator.", "danger")
        return redirect(url_for("dashboard"))

    session.pop("game_completed", None)
    game = Game(player_id=current_user.id, word_id=word.id)
    db.session.add(game)
    db.session.commit()

    session["current_game_id"] = game.id
    return redirect(url_for("game.play"))


@game_bp.route("/play", methods=["GET", "POST"])
def play():
    game_id = session.get("current_game_id")
    if not game_id:
        flash("Start a new game first.", "info")
        return redirect(url_for("dashboard"))

    game = Game.query.get_or_404(game_id)
    game_completed = session.get("game_completed", False)
    if game.completed_at and not game_completed:
        session["game_completed"] = True
        game_completed = True

    guesses = game.guesses.order_by(Guess.attempt_number).all()

    if request.method == "POST":
        if game_completed:
            flash("This game is already finished. Click OK to return to the dashboard.", "info")
            return redirect(url_for("game.play"))

        guess_value = request.form.get("guess", "").strip().upper()
        if len(guess_value) != 5 or not guess_value.isalpha():
            flash("Guess must be exactly 5 uppercase letters.", "danger")
        elif len(guesses) >= MAX_ATTEMPTS:
            flash("Maximum attempts reached.", "warning")
        else:
            attempt_number = len(guesses) + 1
            guess = Guess(game_id=game.id, attempt_number=attempt_number, value=guess_value)
            guess.is_correct = guess_value == game.word.value
            db.session.add(guess)

            if guess.is_correct:
                game.won = True
                game.completed_at = datetime.utcnow()
                session["game_completed"] = True
                flash("Congratulations! You guessed the word.", "success")
            elif attempt_number >= MAX_ATTEMPTS:
                game.won = False
                game.completed_at = datetime.utcnow()
                session["game_completed"] = True
                flash("Better luck next time!", "info")

            db.session.commit()
            return redirect(url_for("game.play"))

        guesses = game.guesses.order_by(Guess.attempt_number).all()

    board = [_build_feedback(guess.value, game.word.value) for guess in guesses]
    while len(board) < MAX_ATTEMPTS:
        board.append([{"letter": "", "status": "empty"} for _ in range(5)])

    return render_template(
        "game.html",
        game=game,
        guesses=guesses,
        board=board,
        max_attempts=MAX_ATTEMPTS,
        game_over=game_completed,
        target_word=game.word.value,
    )


def _build_feedback(guess: str, target: str) -> list[dict[str, str]]:
    statuses = ["absent"] * len(guess)
    counts = Counter(target)

    # First pass: exact matches
    for idx, char in enumerate(guess):
        if char == target[idx]:
            statuses[idx] = "correct"
            counts[char] -= 1

    # Second pass: present but misplaced
    for idx, char in enumerate(guess):
        if statuses[idx] != "absent":
            continue
        if counts[char] > 0:
            statuses[idx] = "present"
            counts[char] -= 1

    return [{"letter": char, "status": statuses[idx]} for idx, char in enumerate(guess)]


@game_bp.route("/finish", methods=["POST"])
@login_required
def finish():
    session.pop("current_game_id", None)
    session.pop("game_completed", None)
    return redirect(url_for("dashboard"))
