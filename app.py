from flask import Flask, jsonify, request, render_template  # 增加了这一项
from flask_sqlalchemy import SQLAlchemy  # 新增
import os


app = Flask(__name__)

# 告诉 Flask 数据库文件存在哪
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义数据库表结构（像画表格一样）
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="未开始")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "status": self.status}


# 定义一个路由：当你访问首页 "/" 时，要做什么
@app.route("/")
def hello():
    return render_template("index.html")  # 让它返回网页

#task函数

@app.route("/tasks", methods=["GET"])
def get_tasks():
    all_tasks = Task.query.all()
    return jsonify([t.to_dict() for t in all_tasks])

#post
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(title=data.get("title"))
    db.session.add(new_task)
    db.session.commit()  # 真正写入文件
    return jsonify(new_task.to_dict()), 201

#updata
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id) # 从数据库找这个任务
    if task:
        task.status = data.get("status", task.status)
        db.session.commit() # 别忘了提交更新！
        return jsonify(task.to_dict())
    return jsonify({"error": "Task not found"}), 404

#delete
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404
# 启动程序
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)