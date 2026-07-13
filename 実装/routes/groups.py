"""
routes/groups.py

グループ管理
"""

import secrets
import string

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db
from models import Group


group_bp = Blueprint(
    "group",
    __name__,
    url_prefix="/group"
)


# =====================================
# 招待コード生成
# =====================================
def create_invite_code(length=8):

    chars = string.ascii_uppercase + string.digits

    while True:

        code = "".join(
            secrets.choice(chars)
            for _ in range(length)
        )

        exists = Group.query.filter_by(
            invite_code=code
        ).first()

        if exists is None:
            return code


# =====================================
# グループ情報
# =====================================
@group_bp.route("/")
@login_required
def group_home():

    return render_template(
        "group.html",
        group=current_user.group
    )


# =====================================
# グループ作成
# =====================================
@group_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_group():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        if name == "":
            flash("グループ名を入力してください。", "danger")
            return redirect(url_for("group.create_group"))

        if current_user.group is not None:
            flash("既にグループへ所属しています。", "warning")
            return redirect(url_for("group.group_home"))

        group = Group(
            name=name,
            invite_code=create_invite_code()
        )

        db.session.add(group)
        db.session.flush()

        current_user.group_id = group.id

        db.session.commit()

        flash("グループを作成しました。", "success")

        return redirect(url_for("group.group_home"))

    return render_template("create_group.html")


# =====================================
# グループ参加
# =====================================
@group_bp.route("/join", methods=["GET", "POST"])
@login_required
def join_group():

    if request.method == "POST":

        code = request.form.get(
            "invite_code",
            ""
        ).strip().upper()

        if current_user.group is not None:

            flash(
                "既にグループへ所属しています。",
                "warning"
            )

            return redirect(
                url_for("group.group_home")
            )

        group = Group.query.filter_by(
            invite_code=code
        ).first()

        if group is None:

            flash(
                "招待コードが存在しません。",
                "danger"
            )

            return redirect(
                url_for("group.join_group")
            )

        current_user.group_id = group.id

        db.session.commit()

        flash(
            f"{group.name} に参加しました。",
            "success"
        )

        return redirect(
            url_for("group.group_home")
        )

    return render_template(
        "join_group.html"
    )


# =====================================
# グループ脱退
# =====================================
@group_bp.route("/leave")
@login_required
def leave_group():

    if current_user.group is None:

        flash(
            "グループに所属していません。",
            "warning"
        )

        return redirect(url_for("index"))

    current_user.group_id = None

    db.session.commit()

    flash(
        "グループを脱退しました。",
        "success"
    )

    return redirect(url_for("index"))