from flask import Flask, render_template, request, redirect, url_for
from models import db, Task
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            task = Task(title=title)
            db.session.add(task)
            db.session.commit()
        return redirect(url_for("index"))

    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Use the port assigned by the platform, or default to 5000 for local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

