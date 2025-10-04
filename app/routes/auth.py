from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db, bcrypt
from ..models import Roles, User
from . import auth_bp


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("game.play"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", Roles.PLAYER)
        if role not in {Roles.PLAYER, Roles.ADMIN}:
            role = Roles.PLAYER

        if not _is_valid_username(username):
            flash(
                "Username must be at least 5 characters, start with a letter, include both upper and lower case, and only use letters or numbers.",
                "danger",
            )
        elif not _is_valid_password(password):
            flash(
                "Password must be at least 5 characters and include a letter, number, and one of $ % * @.",
                "danger",
            )
        elif User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
        else:
            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("game.play"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            if user.is_admin():
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


def _is_valid_username(username: str) -> bool:
    if len(username) < 5:
        return False
    if not username[0].isalpha():
        return False
    if not username.isalnum():
        return False
    has_upper = any(ch.isupper() for ch in username)
    has_lower = any(ch.islower() for ch in username)
    return has_upper and has_lower


def _is_valid_password(password: str) -> bool:
    if len(password) < 5:
        return False
    specials = {"$", "%", "*", "@"}
    has_alpha = any(ch.isalpha() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(ch in specials for ch in password)
    return has_alpha and has_digit and has_special
