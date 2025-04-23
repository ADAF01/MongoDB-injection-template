import os

import pymongo.errors
from flask import Flask, jsonify, render_template_string, request
from pymongo import MongoClient

app = Flask(__name__)

connection_uri = os.environ.get("ATLAS_URI", "mongodb://localhost:27017/")
try:
    client = MongoClient(
        connection_uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000
    )
    client.server_info()
    print(f"[INFO] Connected to MongoDB at {connection_uri}")
except Exception as e:
    raise RuntimeError(f"MongoDB Connection failed: {e}")

db = client["testdb"]
users = db["users"]


def seed_users():
    if users.count_documents({}) == 0:
        users.insert_many(
            [
                {"username": "admin", "password": "secret", "isAdmin": False},
                {"username": "user1", "password": "pass1", "isAdmin": False},
                {"username": "guest", "password": "guest", "isAdmin": False},
            ]
        )


ALLOWED_FIELDS = {"username", "password"}

# Protect Injection func
def sanitize_input(data: dict) -> dict:
    query = {}
    for key in ALLOWED_FIELDS:
        value = data.get(key)
        if isinstance(value, str) and value:
            query[key] = value
    return query


@app.route("/login", methods=["GET"])
def login_get():
    query = request.args.to_dict(flat=True)
    # raw = request.args.to_dict(flat=False)
    # query = sanitize_input(raw)
    # if len(query) != len(ALLOWED_FIELDS):
    #     return jsonify([]), 400
    result = list(users.find(query, {"_id": 0}))
    return jsonify(result)


@app.route("/login", methods=["POST"])
def login_post():
    query = request.get_json(force=True)
    if not query:
        return jsonify([]), 400
    # raw = request.get_json(force=True) or {}
    # query = sanitize_input(raw)
    # if len(query) != len(ALLOWED_FIELDS):
    #     return jsonify([]), 400
    result = list(users.find(query, {"_id": 0}))
    return jsonify(result)


HTML = """
<html>
  <body>
    <h2>Login Test (GET)</h2>
    <form action="/login" method="get">
      Username: <input name="username"><br>
      Password: <input name="password"><br>
      <input type="submit" value="Login">
    </form>

    <h2>Login Test (POST)</h2>
    <form id="postForm">
      Username: <input id="u" name="username"><br>
      Password: <input id="p" name="password"><br>
      <button type="button" onclick="send()">Login</button>
    </form>
    <pre id="res"></pre>
    <script>
      function send() {
        const u = document.getElementById('u').value;
        const p = document.getElementById('p').value;
        fetch('/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: u, password: p })
        })
        .then(r => r.json())
        .then(d => document.getElementById('res').innerText = JSON.stringify(d, null, 2));
      }
    </script>
  </body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


if __name__ == "__main__":
    seed_users()
    app.run(host="0.0.0.0", port=5000, debug=True)
