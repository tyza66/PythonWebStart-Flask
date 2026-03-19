from __future__ import annotations

import os
import tempfile
from typing import Dict, Any
from flask import Flask, request, jsonify, abort


def create_app(test_config: Dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)

    app.config["USERS"] = []

    # 返回Json格式的数据
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    # 接收路径参数的Get请求接口
    @app.route("/items/<int:item_id>", methods=["GET"])
    def get_item(item_id: int):
        item = {"item_id": item_id, "name": f"Item {item_id}", "price": 9.99}
        return jsonify(item), 200

    # 携带查询参数（query参数、params）的Get请求接口 这里是 q 和 limit
    @app.route("/search", methods=["GET"])
    def search():
        q = request.args.get("q")
        if not q: # 如果没有提供q参数，返回400错误
            return jsonify({"error": "query parameter 'q' is required"}), 400
        try:
            limit = int(request.args.get("limit", 10))
        except ValueError:
            return jsonify({"error": "query parameter 'limit' must be an integer"}), 400

        results = [{"id": i, "title": f"{q} result {i}"} for i in range(1, limit + 1)]
        return jsonify({"q": q, "limit": limit, "results": results}), 200

    ### Header参数的Get请求接口
    @app.route("/whoami", methods=["GET"])
    def whoami():
        user = request.headers.get("X-User") # 从请求头中获取X-User字段
        if not user:
            return jsonify({"error": "Missing header X-User"}), 400
        return jsonify({"message": f"Hello, {user}!"}), 200

    # 处理JSON请求体的POST请求接口
    # 可用的Json模板⬇️
    '''
    {
    "name": "John Doe",
    "email": "jd@test.com"
    }
    '''
    @app.route("/users", methods=["POST"])
    def create_user():
        if not request.is_json:
            return jsonify({"error": "Expected application/json"}), 415

        payload = request.get_json()
        name = payload.get("name")
        email = payload.get("email")
        # 进行简单的检查
        if not name or not email:
            return jsonify({"error": "Both 'name' and 'email' are required"}), 400

        user_id = len(app.config["USERS"]) + 1
        user = {"id": user_id, "name": name, "email": email}
        app.config["USERS"].append(user)
        return jsonify(user), 201

    # 处理表单数据的POST请求接口
    @app.route("/login", methods=["POST"])
    def login():
        username = request.form.get("username")
        password = request.form.get("password")
        # 简单检查
        if not username or not password:
            return jsonify({"error": "Both 'username' and 'password' are required"}), 400

        # 模拟认证成功 返回一个假的token
        token = f"token-{username}-12345"
        return jsonify({"username": username, "token": token}), 200

    # 处理文件上传的POST请求接口
    @app.route("/upload", methods=["POST"])
    def upload_file():
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request (field 'file')"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        tmpdir = tempfile.gettempdir()
        save_path = os.path.join(tmpdir, file.filename)
        file.save(save_path)
        size = os.path.getsize(save_path)
        return jsonify({"filename": file.filename, "saved_to": save_path, "size": size}), 201
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=7001, debug=True)
