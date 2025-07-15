import random
from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("main", __name__)

CARD_POOL = list(range(120))          # 0‒119 共 120 张
SPECIAL_SET = {0, 15, 71, 100, 50, 51, 66, 77}

# ---------- 首页 ----------
@bp.route("/")
def index():
    return render_template("index.html", message="德州皇室玩法，灵感来源Xiake - Youtube")

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
    """返回 (public_pool, private_pool) 按规则限制特殊牌出现次数。"""
    rng = random.Random(seed)
    cards = CARD_POOL.copy()
    rng.shuffle(cards)

    public_pool, private_pool = [], []
    pub_specials = 0
    priv_specials = 0
    i = 0

    # —— 先凑满公共 8 张 —— #
    while len(public_pool) < 8 and i < len(cards):
        c = cards[i]; i += 1
        if c in SPECIAL_SET:
            if pub_specials == 0:
                public_pool.append(c)
                pub_specials = 1
            # 若已超额，跳过这张继续扫描
        else:
            public_pool.append(c)

    # —— 再凑满私人 4 张 —— #
    while len(private_pool) < 4 and i < len(cards):
        c = cards[i]; i += 1
        if c in SPECIAL_SET:
            if priv_specials == 0:
                private_pool.append(c)
                priv_specials = 1
        else:
            private_pool.append(c)

    # 理论上卡库足够大，一定能拿齐 12 张；如保险可加兜底判断

    return public_pool, private_pool
