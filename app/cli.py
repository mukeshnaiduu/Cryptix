import click

from .extensions import db
from .models import Roles, User, Word
from .seeds import DEFAULT_WORDS


def _seed_words(force: bool) -> int:
    if force:
        Word.query.delete()

    inserted = 0
    for value in DEFAULT_WORDS:
        value = value.upper()
        if not Word.query.filter_by(value=value).first():
            db.session.add(Word(value=value))
            inserted += 1

    db.session.commit()
    return inserted


def init_cli(app):
    @app.cli.command("init-db")
    @click.option("--with-words/--no-words", default=True, help="Seed default words after creating tables.")
    def init_db(with_words: bool) -> None:
        """Create all database tables."""
        db.create_all()
        message = "Database initialized."
        if with_words:
            inserted = _seed_words(force=False)
            message += f" Seeded {inserted} words."
        click.echo(message)

    @app.cli.command("seed-words")
    @click.option("--force", is_flag=True, help="Replace existing words.")
    def seed_words(force: bool) -> None:
        """Populate the words table with the default 20 entries."""
        inserted = _seed_words(force=force)
        click.echo(f"Seeded {inserted} words (force={force}).")

    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("password")
    def create_admin(username: str, password: str) -> None:
        """Create an admin user quickly via the CLI."""
        if User.query.filter_by(username=username).first():
            raise click.ClickException("Username already exists.")

        from .routes.auth import _is_valid_password, _is_valid_username

        if not _is_valid_username(username):
            raise click.ClickException(
                "Username must be at least 5 characters, start with a letter, include upper and lower case, and contain only letters or numbers."
            )

        if not _is_valid_password(password):
            raise click.ClickException(
                "Password must be at least 5 chars and include letters, numbers, and one of $ % * @." 
            )

        user = User(username=username, role=Roles.ADMIN)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo("Admin user created successfully.")
