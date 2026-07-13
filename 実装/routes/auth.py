"""
routes/auth.py

ユーザー認証
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from extensions import db
from models import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# ==========================
# 新規登録
# ==========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    # ログイン済みならトップへ
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        pin = request.form.get("pin", "").strip()

        # ----------------------
        # バリデーション
        # ----------------------

        if username == "":
            flash("ユーザー名を入力してください。", "danger")
            return redirect(url_for("auth.register"))

        if len(pin) != 4 or not pin.isdigit():
            flash("PINは4桁の数字で入力してください。", "danger")
            return redirect(url_for("auth.register"))

        # ----------------------
        # 重複チェック
        # ----------------------

        exists = User.query.filter_by(
            username=username
        ).first()

        if exists:
            flash("そのユーザー名は既に使用されています。", "danger")
            return redirect(url_for("auth.register"))

        # ----------------------
        # 登録
        # ----------------------

        user = User(
            username=username
        )

        user.set_pin(pin)

        db.session.add(user)
        db.session.commit()

        flash("登録が完了しました。ログインしてください。", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ==========================
# ログイン
# ==========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        pin = request.form.get("pin", "").strip()

        user = User.query.filter_by(
            username=username
        ).first()

        # ----------------------
        # 認証
        # ----------------------

        if user is None:
            flash("ユーザー名またはPINが違います。", "danger")
            return redirect(url_for("auth.login"))

        if not user.check_pin(pin):
            flash("ユーザー名またはPINが違います。", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)

        flash("ログインしました。", "success")

        return redirect(url_for("index"))

    return render_template("login.html")


# ==========================
# ログアウト
# ==========================
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("ログアウトしました。", "info")

    return redirect(url_for("auth.login"))