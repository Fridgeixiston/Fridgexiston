import sqlite3
from flask import g
import os

# データベースファイルの保存先（instanceフォルダ内）
DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'fridgexiston.db')

def get_db():
    """データベース接続を取得する"""
    db = getattr(g, '_database', None)
    if db is None:
        # instanceフォルダが存在しない場合は作成
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE)
        # 列名でアクセスできるようにする設定
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    """リクエスト終了時にデータベース接続を閉じる"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """テーブルを作成する（初回のみ）"""
    db = get_db()
    cursor = db.cursor()
    
    # グループテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ユーザーテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pin_code TEXT NOT NULL,
            group_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        )
    ''')
    
    # 食材・買い物リストテーブル
    # status は 'stock'(在庫) または 'buy'(買うリスト) が入る想定
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity TEXT,
            status TEXT NOT NULL,
            group_id INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        )
    ''')
    
    db.commit()