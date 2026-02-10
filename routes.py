from flask import Blueprint, request, jsonify
from models import db, Task

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.completed = data.get("completed", task.completed)

    db.session.commit()
    return jsonify(task.to_dict())

@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
