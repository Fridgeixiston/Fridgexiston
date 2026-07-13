from flask import Blueprint, request, redirect, flash
from app import db
from models import StockItem

stock_bp = Blueprint(
    "stock",
    __name__,
    url_prefix="/stock"
)


# ------------------------
# 在庫追加
# ------------------------
@stock_bp.route("/add", methods=["POST"])
def add_stock():

    name = request.form["name"]
    quantity = int(request.form["quantity"])

    stock = StockItem.query.filter_by(
        name=name,
        group_id=1
    ).first()

    if stock:

        stock.quantity += quantity

    else:

        stock = StockItem(
            name=name,
            quantity=quantity,
            group_id=1
        )

        db.session.add(stock)

    db.session.commit()

    flash("在庫を追加しました")

    return redirect("/")


# ------------------------
# 在庫削除
# ------------------------
@stock_bp.route("/delete/<int:id>")
def delete_stock(id):

    stock = StockItem.query.get_or_404(id)

    db.session.delete(stock)

    db.session.commit()

    flash("削除しました")

    return redirect("/")