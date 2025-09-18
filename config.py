# mysite/config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-prod")
    SITE_TITLE = "Clash Royale Deck Helper"
    LANGUAGES = {"zh": "中文", "en": "English"}

    # 新增：临时切换德扑桌
    SHOW_POKER = os.environ.get("SHOW_POKER", "0") == "1"
