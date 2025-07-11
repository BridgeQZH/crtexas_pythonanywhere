# __init__.py
from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # 注册蓝图
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app


# 供 WSGI 入口直接导入
app = create_app()
