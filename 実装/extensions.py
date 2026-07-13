"""
extensions.py

Flaskの拡張機能を管理するファイル
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# データベース
db = SQLAlchemy()

# ログイン管理
login_manager = LoginManager()

# ログインしていない場合の遷移先
login_manager.login_view = "auth.login"

# メッセージ
login_manager.login_message = "ログインしてください。"
login_manager.login_message_category = "warning"

# データベースマイグレーション
migrate = Migrate()