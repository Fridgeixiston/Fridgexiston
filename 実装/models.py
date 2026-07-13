"""
models.py

データベースモデル
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


# ======================================
# グループ
# ======================================
class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)

    # ○○家
    name = db.Column(db.String(50), nullable=False)

    # 招待コード
    invite_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # リレーション
    users = db.relationship(
        "User",
        back_populates="group",
        lazy=True
    )

    shopping_items = db.relationship(
        "ShoppingItem",
        back_populates="group",
        cascade="all, delete"
    )

    stock_items = db.relationship(
        "StockItem",
        back_populates="group",
        cascade="all, delete"
    )

    notifications = db.relationship(
        "Notification",
        back_populates="group",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Group {self.name}>"



# ======================================
# ユーザー
# ======================================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    # ハッシュ化したPIN
    pin_hash = db.Column(
        db.String(255),
        nullable=False
    )

    group_id = db.Column(
        db.Integer,
        db.ForeignKey("groups.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    group = db.relationship(
        "Group",
        back_populates="users"
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user"
    )

    # -------------------------
    # PIN保存
    # -------------------------
    def set_pin(self, pin):
        self.pin_hash = generate_password_hash(pin)

    # -------------------------
    # PIN確認
    # -------------------------
    def check_pin(self, pin):
        return check_password_hash(
            self.pin_hash,
            pin
        )

    def __repr__(self):
        return f"<User {self.username}>"



# ======================================
# 買い物リスト
# ======================================
class ShoppingItem(db.Model):
    __tablename__ = "shopping_items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(50),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    category = db.Column(
        db.String(30)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    group_id = db.Column(
        db.Integer,
        db.ForeignKey("groups.id"),
        nullable=False
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    group = db.relationship(
        "Group",
        back_populates="shopping_items"
    )

    def __repr__(self):
        return f"<ShoppingItem {self.name}>"



# ======================================
# 在庫
# ======================================
class StockItem(db.Model):
    __tablename__ = "stock_items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(50),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    category = db.Column(
        db.String(30)
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    group_id = db.Column(
        db.Integer,
        db.ForeignKey("groups.id"),
        nullable=False
    )

    group = db.relationship(
        "Group",
        back_populates="stock_items"
    )

    def __repr__(self):
        return f"<StockItem {self.name}>"



# ======================================
# 通知
# ======================================
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(
        db.String(255),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    group_id = db.Column(
        db.Integer,
        db.ForeignKey("groups.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    group = db.relationship(
        "Group",
        back_populates="notifications"
    )

    user = db.relationship(
        "User",
        back_populates="notifications"
    )

    def __repr__(self):
        return f"<Notification {self.message}>"