from __future__ import annotations

from typing import Dict, Any
from flask import Flask, render_template


def create_app(test_config: Dict[str, Any] | None = None) -> Flask:
    """Create a small Flask app that serves index.html and model.html with data."""

    # Use project root as template folder so existing HTML files are found directly
    app = Flask(__name__, template_folder='.')

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/model')
    def model():
        data = {
            'title': '这是一个动态模板标题',
            'user': {'name': '小明', 'role': 'tester'},
            'items': [
                {'id': 1, 'name': '苹果'},
                {'id': 2, 'name': '香蕉'},
                {'id': 3, 'name': '橘子'},
            ]
        }
        return render_template('model.html', **data)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=7001, debug=True)

