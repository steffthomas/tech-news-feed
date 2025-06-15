from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingCodeError
from . import db
from .models import User, Article
from .scraper.hackernews import get_hackernews_articles
from .scraper.techcrunch import get_techcrunch_articles
import os

main = Blueprint('main', __name__)

# Google OAuth Blueprint with full scope
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ],
    redirect_to="main.dashboard"
)

# Prevent Flask-Dance from throwing scope mismatch errors
@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        print("❌ Failed to log in with Google.")
        return False
    return True

main.register_blueprint(google_bp, url_prefix="/login")


@main.route("/")
def home():
    return render_template("login.html")


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not google.authorized:
        return redirect(url_for("main.google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Failed to fetch user info.", 400

    user_info = resp.json()
    google_id = user_info["id"]
    email = user_info["email"]

    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(google_id=google_id, email=email)
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id

    if request.method == "POST":
        title = request.form.get("title")
        link = request.form.get("link")
        summary = request.form.get("summary")
        source = request.form.get("source")
        existing = Article.query.filter_by(user_id=user.id, link=link).first()
        if not existing:
            article = Article(
                title=title,
                link=link,
                summary=summary,
                source=source,
                user_id=user.id
            )
            db.session.add(article)
            db.session.commit()

    scraped_articles = get_hackernews_articles() + get_techcrunch_articles()
    return render_template("dashboard.html", articles=scraped_articles)


@main.route("/saved")
def saved_articles():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("main.home"))

    articles = Article.query.filter_by(user_id=user_id).all()
    return render_template("saved.html", articles=articles)
