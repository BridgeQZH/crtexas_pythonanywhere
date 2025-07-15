# config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-prod")
    SITE_TITLE = "CR Texas 德州皇室"
    LANGUAGES = {"zh": "中文", "en": "English"}     # ← 新增
