import json
from flask import Flask
from flask import request
from db import db, Artist, Album, Song
from controller import """ """

"""
What we need:

file.db
controller.py
"""
app = Flask(__name__)
db_filename = 'spotify.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def start():
    return 'Spotify Clone'

# @app.route("/tasks/")
# def get_tasks():
#     """
#     Returns all tasks
#     """
#     res =  {"tasks": list(tasks.values())}
#     return res
#
# @app.route("/posts/", methods = ["POST"])
# def create_post():
#     """
#     Creates a new task
#     """
#     global post_id_counter
#     body = json.loads(request.data)
#     title = body.get("title")
#     link = body.get("link")
#     username = body.get("username")
#
#     post = {
#         "id": task_id_counter,
#         "upvotes": 1,
#         "title": title,
#         "link": link,
#         "username": username
#     }
#
#     posts[post_id_counter] = task
#     post_id_counter +=1
#     return json.dumps(post)
#
# @app.route("/posts/<int:post_id>/")
# def get_post(post_id):
#     """
#     Gets posts by id
#     """
#     post = posts.get(post_id)
#     if post is None:
#         return json.dumps({"error": "Post not found!"}), 404
#     return json.dumps(post), 200
#
# @app.route("/posts/<int:post_id>/", methods = ["DELETE"])
# def delete_post(post_id):
#     """
#     deletes posts by id
#     """
#     post = posts.get(post_id)
#     if post is None:
#         return json.dumps({"error": "Post not found!"}), 404
#     del posts[post_id]
#     return json.dumps(post), 200
#
# app.route("/posts/<int:post_id>/comments", methods = ["POST"])
# def update_Post(post_id):
#     """
#     Updates tasks by id
#     """
#     post = posts.get(post_id)
#     if task is None:
#         return json.dumps({"error": "Task not found!"}), 404
#
#     body = json.loads(request.data)
#
#     description = body.get("description")
#     done = body.get("done")
#     task["description"] = description
#     task["done"] = done
#     return json.dumps(task), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
