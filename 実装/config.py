import os

# プロジェクトのルートディレクトリ
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """アプリケーション共通設定"""

    # Flask
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "fridgexiston_secret_key"
    )

    # SQLiteデータベース
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "database.db")
    )

    # SQLAlchemy設定
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask設定
    JSON_AS_ASCII = False

    # デバッグモード
    DEBUG = True