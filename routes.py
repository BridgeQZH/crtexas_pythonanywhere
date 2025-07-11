# routes.py
from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    # message 只是示范，可替换成数据库或其他动态内容
    return render_template("index.html", message="Hello from Flask! Zihan at Malmö 🇸🇪")
