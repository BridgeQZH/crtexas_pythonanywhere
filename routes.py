import random
from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("main", __name__)

CARD_POOL = list(range(120))          # 0‒119 共 120 张

# ---------- 首页 ----------
@bp.route("/")
def index():
    return render_template("index.html", message="Hello from Flask! Zihan at Malmö 🇸🇪")

# ---------- 处理表单 ----------
@bp.route("/start", methods=["POST"])
def start_game():
    seed = request.form.get("seed", "").strip()
    color = request.form.get("color")

    if not (seed.isdigit() and len(seed) == 4):
        flash("请输入 0000-9999 的四位数字")
        return redirect(url_for("main.index"))

    if color not in ("blue", "red"):
        return redirect(url_for("main.index"))

    return redirect(url_for("main.game", color=color, seed=seed))

# ---------- 游戏页面 ----------
@bp.route("/game/<color>")
def game(color):
    seed = request.args.get("seed")
    if color not in ("blue", "red") or seed is None:
        return redirect(url_for("main.index"))

    public_pool, private_pool = deal_cards(int(seed), color)

    return render_template(
        "game.html",
        color=color,
        public_pool=public_pool,
        private_pool=private_pool,
    )

# ---------- 发牌 ----------
def deal_cards(seed: int, color: str):
    rng = random.Random(seed)
    cards = CARD_POOL.copy()
    rng.shuffle(cards)

    public_pool = cards[:8]                 # 公共 8 张
    private_pool = cards[8:12] if color == "blue" else cards[12:16]
    return public_pool, private_pool
