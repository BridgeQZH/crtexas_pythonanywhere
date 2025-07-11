# routes.py
import random
from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("main", __name__)

# 简单的“牌库”，先用数字占位；以后换成你的 100+ 张卡名字或图片路径
CARD_POOL = list(range(1, 105))    # 1‒104 共 104 张牌示例

@bp.route("/")
def index():
    return render_template("index.html", message="Hello from Flask! Zihan at Malmö 🇸🇪")

# 处理表单 POST
@bp.route("/start", methods=["POST"])
def start_game():
    seed = request.form.get("seed", "").strip()
    color = request.form.get("color")

    if not (seed.isdigit() and len(seed) == 4):
        flash("请输入 0000-9999 的四位数字")
        return redirect(url_for("main.index"))

    if color not in ("blue", "red"):
        return redirect(url_for("main.index"))

    # 把种子和身份塞进查询串 -> /game/blue?seed=1234
    return redirect(url_for("main.game", color=color, seed=seed))


@bp.route("/game/<color>")
def game(color):
    seed = request.args.get("seed")
    if color not in ("blue", "red") or seed is None:
        return redirect(url_for("main.index"))

    # 发牌：公共 8 张 + 私人 4 张（互不重复）
    public_pool, private_pool = deal_cards(int(seed), color)

    return render_template(
        "game.html",
        color=color,
        public_pool=public_pool,
        private_pool=private_pool,
    )


def deal_cards(seed: int, color: str):
    """同一 seed 下，公共池对红蓝一致；私人池互不重叠"""
    rng = random.Random(seed)
    cards = CARD_POOL.copy()
    rng.shuffle(cards)

    public_pool = cards[:8]              # 前 8 张 → 公共
    if color == "blue":
        private_pool = cards[8:12]       # 蓝拿第 9‒12
    else:
        private_pool = cards[12:16]      # 红拿第 13‒16
    return public_pool, private_pool
