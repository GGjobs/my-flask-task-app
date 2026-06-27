# my-flask-task-app

一个基于 Flask 的简易任务管理 Web 应用，支持创建任务、查看任务列表和切换任务完成状态。项目使用 SQLite 保存数据，适合用来练习 Flask 路由、REST API、模板页面和 SQLAlchemy 数据模型。

## 功能

- 添加任务
- 查看任务列表
- 点击任务切换 `未开始` / `已完成`
- 使用 SQLite 持久化任务数据
- 提供前后端一体的简单页面

## 技术栈

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML / CSS / JavaScript
- Gunicorn

## 项目结构

```text
.
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

## 本地运行

创建虚拟环境并安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

启动应用：

```bash
python app.py
```

默认访问：

```text
http://127.0.0.1:5000
```

## API

### 获取任务列表

```http
GET /tasks
```

### 新增任务

```http
POST /tasks
Content-Type: application/json

{
  "title": "学习 Flask"
}
```

### 更新任务状态

```http
PUT /tasks/{task_id}
Content-Type: application/json

{
  "status": "已完成"
}
```

## 数据库

应用启动时会自动在项目目录下创建 `tasks.db`。该文件是本地运行数据，不建议提交到仓库。

## 部署说明

`requirements.txt` 中包含 `gunicorn`，可以用于云平台部署：

```bash
gunicorn app:app
```

如果部署平台提供 `PORT` 环境变量，`app.py` 中也已经兼容该配置。
