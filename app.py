import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- 关键修改 1：使用绝对路径定死数据库位置 ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), default="未开始")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "status": self.status}

# --- 关键修改 2：在程序启动前强制创建数据库文件 ---
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "缺少标题"}), 400
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if task:
        task.status = data.get("status", task.status)
        db.session.commit()
        return jsonify(task.to_dict())
    return jsonify({"error": "任务未找到"}), 404

if __name__ == "__main__":
    # 云端通常由 gunicorn 运行，但保留此项用于本地测试
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
