import os, json, random
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, g, current_app
)

bp = Blueprint("main", __name__)

# ---------- 0.  翻译字典 ----------
_trans = {
    "zh": {
        "seed_ph":  "输入 4 位数字种子 (0000-9999)",
        "blue_btn": "我是蓝国王",
        "red_btn":  "我是红国王",
        "public":   "公共卡池（8 张）",
        "priv_b":   "私人卡池（4 张，仅 蓝国王 可见）",
        "priv_r":   "私人卡池（4 张，仅 红国王 可见）",
        "tower":    "选择塔楼部队",
        "copy":     "复制该卡组",
        "restart":  "重新开始"
    },
    "en": {
        "seed_ph":  "Enter 4‑digit seed (0000‑9999)",
        "blue_btn": "I am Blue King",
        "red_btn":  "I am Red King",
        "public":   "Public pool (8 cards)",
        "priv_b":   "Private pool (4 cards, Blue only)",
        "priv_r":   "Private pool (4 cards, Red only)",
        "tower":    "Choose Tower",
        "copy":     "Copy Deck",
        "restart":  "Restart"
    }
}

# ---------- 1.  在每个请求前确定语言 ----------
@bp.before_app_request
def detect_lang():
    g.lang = session.get("lang", "zh")            # 默认为中文


# ---------- 2.  提供简易翻译函数给模板 ----------
@bp.app_context_processor
def inject_t():
    def t(key):                                   # 用法：{{ t('public') }}
        return _trans.get(g.lang, _trans["zh"]).get(key, key)
    return dict(t=t, lang=g.lang)


# ---------- 3.  切换语言的路由 ----------
@bp.route("/lang/<lang_code>")
def set_lang(lang_code):
    if lang_code in _trans:
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("main.index"))


CARD_POOL = list(range(120))          # 0‒119 共 120 张

# ---------- 首页 ----------
@bp.route("/")
def index():
    # 如果开关打开，显示德扑桌；否则显示原来的皇室首页
    if current_app.config.get("SHOW_POKER"):
        seats = load_seats()
        return render_template("poker.html", seats=seats)
    return render_template("index.html")

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

def load_seats():
    """从 data/seating.json 读取10个座位字符串，不足则用 'empty' 补齐。"""
    data_path = os.path.join(os.path.dirname(__file__), "data", "seating.json")
    seats = ["empty"] * 10
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        if isinstance(obj, dict) and "seats" in obj:
            raw = obj["seats"]
        elif isinstance(obj, list):
            raw = obj
        else:
            raw = []
        seats = (raw + ["empty"] * 10)[:10]
    except Exception:
        pass
    return seats