"""
app.py

Fridgexiston メインアプリケーション
"""

from flask import Flask, render_template

from config import Config
from extensions import db
from extensions import login_manager
from extensions import migrate

# モデルを読み込む（create_all()のため）
from models import User

# Blueprint
from routes.auth import auth_bp
from routes.groups import group_bp
from routes.shopping import shopping_bp
from routes.stock import stock_bp


def create_app():
    app = Flask(__name__)

    # ==========================
    # Config
    # ==========================
    app.config.from_object(Config)

    # ==========================
    # Extension初期化
    # ==========================
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # ==========================
    # Blueprint登録
    # ==========================
    app.register_blueprint(auth_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(shopping_bp)
    app.register_blueprint(stock_bp)

    # ==========================
    # トップページ
    # ==========================
    @app.route("/")
    def index():
        return render_template("index.html")

    # ==========================
    # データベース生成
    # ==========================
    with app.app_context():
        db.create_all()

    return app


# ==========================
# Flask-Login
# ==========================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==========================
# アプリ起動
# ==========================
app = create_app()

if __name__ == "__main__":
    app.run()