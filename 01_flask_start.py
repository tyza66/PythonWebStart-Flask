# 看一下效果，知道啥是Web Api
from flask import Flask

app = Flask(__name__)

# 定义一个路由，访问根路径时返回 "Hello, World!" 这些文字
@app.route("/")
def hello():
    return "Hello, World!"

app.run(host="0.0.0.0", port=7001)