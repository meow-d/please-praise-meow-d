from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS posts (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      content TEXT NOT NULL
                    )"""
    )
    conn.commit()
    conn.close()


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


@app.route("/praises", methods=["GET"])
def get_posts():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = [{"id": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify(posts), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
