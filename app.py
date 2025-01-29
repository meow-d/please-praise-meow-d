import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify, abort, render_template


DATABASE = "database.db"
ALLOWED_EXTENSIONS = {"png", "webp"}

env = load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
PRODUCTION = os.getenv("PRODUCTION")

app = Flask(
    __name__, static_url_path="/", static_folder="static", template_folder="static"
)
app.config["UPLOAD_FOLDER"] = "static/draws/"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS draws (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )"""
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/praise", methods=["POST"])
def create_post():
    if not request.json:
        return jsonify({"error": "The request is not JSON"}), 400

    content = request.json.get("content")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (content) VALUES (?)", (content,))
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": post_id, "content": content}), 201


@app.route("/praise-with-presets", methods=["POST"])
def create_post_but_for_losers():
    a = request.form.get("a")
    b = request.form.get("b")
    c = request.form.get("c")
    d = request.form.get("action")

    # WONTFIX cause funny
    content = f"{a} {b} {c} {d}".strip()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

    return redirect("/thank-you.html")


@app.route("/praises", methods=["GET"])
def get_posts():
    auth_token = request.headers.get("Authorization")
    if auth_token != SECRET_TOKEN:
        abort(403)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = [{"id": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify(posts), 200


@app.route("/draw", methods=["GET", "POST"])
def create_draw():
    if request.method == "GET":
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM draws")
        images = cursor.fetchall()
        conn.close()
        return render_template("draw.html", images=images)

    if "image" not in request.files:
        return jsonify({"error": "Content is requried"}, 400)
    image = request.files["image"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO draws DEFAULT VALUES")
    id = cursor.lastrowid

    path = os.path.join(app.config["UPLOAD_FOLDER"], f"{id}.png")
    image.save(path)
    conn.commit()
    conn.close()

    return redirect(request.url)


if __name__ == "__main__":
    init_db()
    if PRODUCTION != "true":
        app.run(host="0.0.0.0", port=3000)
