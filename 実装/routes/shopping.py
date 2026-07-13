"""
routes/shopping.py

買い物リスト管理
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
    login_required,
    current_user
)

from extensions import db
from models import ShoppingItem


shopping_bp = Blueprint(
    "shopping",
    __name__,
    url_prefix="/shopping"
)


# ======================================
# 買い物リスト一覧
# ======================================
@shopping_bp.route("/")
@login_required
def shopping_list():

    if current_user.group is None:

        flash(
            "先にグループへ参加してください。",
            "warning"
        )

        return redirect(
            url_for("group.create_group")
        )

    items = (
        ShoppingItem.query
        .filter_by(group_id=current_user.group_id)
        .order_by(ShoppingItem.created_at.desc())
        .all()
    )

    return render_template(
        "shopping.html",
        items=items
    )


# ======================================
# 食材追加
# ======================================
@shopping_bp.route("/add", methods=["POST"])
@login_required
def add_item():

    if current_user.group is None:

        flash(
            "グループへ参加してください。",
            "warning"
        )

        return redirect(
            url_for("group.create_group")
        )

    name = request.form.get("name", "").strip()

    quantity = request.form.get(
        "quantity",
        1,
        type=int
    )

    category = request.form.get(
        "category",
        ""
    ).strip()

    if name == "":

        flash(
            "食材名を入力してください。",
            "danger"
        )

        return redirect(
            url_for("shopping.shopping_list")
        )

    if quantity <= 0:

        flash(
            "数量は1以上を入力してください。",
            "danger"
        )

        return redirect(
            url_for("shopping.shopping_list")
        )

    # 同じ食材なら数量を加算
    item = ShoppingItem.query.filter_by(
        group_id=current_user.group_id,
        name=name
    ).first()

    if item:

        item.quantity += quantity

    else:

        item = ShoppingItem(
            name=name,
            quantity=quantity,
            category=category,
            group_id=current_user.group_id,
            created_by=current_user.id
        )

        db.session.add(item)

    db.session.commit()

    flash(
        "買い物リストへ追加しました。",
        "success"
    )

    return redirect(
        url_for("shopping.shopping_list")
    )


# ======================================
# 編集
# ======================================
@shopping_bp.route(
    "/edit/<int:item_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_item(item_id):

    item = ShoppingItem.query.get_or_404(item_id)

    if item.group_id != current_user.group_id:

        flash(
            "アクセス権限がありません。",
            "danger"
        )

        return redirect(
            url_for("shopping.shopping_list")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        quantity = request.form.get(
            "quantity",
            1,
            type=int
        )

        category = request.form.get(
            "category",
            ""
        ).strip()

        if name == "":

            flash(
                "食材名を入力してください。",
                "danger"
            )

            return redirect(
                url_for(
                    "shopping.edit_item",
                    item_id=item.id
                )
            )

        item.name = name
        item.quantity = quantity
        item.category = category

        db.session.commit()

        flash(
            "更新しました。",
            "success"
        )

        return redirect(
            url_for("shopping.shopping_list")
        )

    return render_template(
        "edit_shopping.html",
        item=item
    )


# ======================================
# 削除
# ======================================
@shopping_bp.route("/delete/<int:item_id>")
@login_required
def delete_item(item_id):

    item = ShoppingItem.query.get_or_404(item_id)

    if item.group_id != current_user.group_id:

        flash(
            "アクセス権限がありません。",
            "danger"
        )

        return redirect(
            url_for("shopping.shopping_list")
        )

    db.session.delete(item)

    db.session.commit()

    flash(
        "削除しました。",
        "success"
    )

    return redirect(
        url_for("shopping.shopping_list")
    )

# ======================================
# 購入完了
# 買い物リスト → 在庫へ移動
# ======================================
from sqlalchemy.exc import SQLAlchemyError
from models import StockItem, Notification


@shopping_bp.route("/complete/<int:item_id>", methods=["POST"])
@login_required
def complete_item(item_id):

    item = ShoppingItem.query.get_or_404(item_id)

    # --------------------------
    # グループチェック
    # --------------------------
    if item.group_id != current_user.group_id:

        flash(
            "アクセス権限がありません。",
            "danger"
        )

        return redirect(
            url_for("shopping.shopping_list")
        )

    try:

        # --------------------------
        # 在庫に同じ食材があるか確認
        # --------------------------
        stock = StockItem.query.filter_by(
            group_id=current_user.group_id,
            name=item.name
        ).first()

        if stock:

            # 数量加算
            stock.quantity += item.quantity

        else:

            # 新規在庫追加
            stock = StockItem(
                name=item.name,
                quantity=item.quantity,
                category=item.category,
                group_id=current_user.group_id
            )

            db.session.add(stock)

        # --------------------------
        # 通知作成
        # --------------------------
        notification = Notification(
            message=f"{current_user.username}さんが「{item.name}」を購入しました。",
            group_id=current_user.group_id,
            user_id=current_user.id
        )

        db.session.add(notification)

        # --------------------------
        # 買い物リストから削除
        # --------------------------
        db.session.delete(item)

        # --------------------------
        # 保存
        # --------------------------
        db.session.commit()

        flash(
            "購入完了しました。",
            "success"
        )

    except SQLAlchemyError:

        db.session.rollback()

        flash(
            "購入処理に失敗しました。",
            "danger"
        )

    return redirect(
        url_for("shopping.shopping_list")
    )
    
    
    