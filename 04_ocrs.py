from __future__ import annotations

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

def create_app() -> Flask:
    # 创建一个Flask应用，并启用CORS以允许所有来源的请求
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route('/')
    def demo():
        return jsonify({"message": "This response allows CORS from any origin."})

    return app

if __name__ == '__main__':
    app = create_app()
    # Run on 0.0.0.0:7002 per your request
    app.run(host='0.0.0.0', port=7002, debug=True)

