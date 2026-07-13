from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# リクエストが終わるたびにDB接続を閉じる設定
app.teardown_appcontext(database.close_connection)

# アプリ起動時にテーブルを作成する
with app.app_context():
    database.init_db()

# --- ルーティング（画面遷移と処理） ---

@app.route('/')
def index():
    # ひとまず在庫一覧画面へリダイレクト
    return redirect(url_for('inventory'))


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    db = database.get_db()
    group_id = 1 # ※一旦グループID=1で固定してテストします

    if request.method == 'POST':
        # フォームから送信されたデータを受け取り、在庫（stock）としてDBに登録
        name = request.form.get('name')
        quantity = request.form.get('quantity', '')
        
        if name: # 名前が入力されている場合のみ保存
            db.execute('''
                INSERT INTO items (name, quantity, status, group_id)
                VALUES (?, ?, 'stock', ?)
            ''', (name, quantity, group_id))
            db.commit()
        return redirect(url_for('inventory'))

    # GETリクエスト時：DBから在庫リストを取得して画面に渡す
    items = db.execute('''
        SELECT * FROM items 
        WHERE status = 'stock' AND group_id = ? 
        ORDER BY updated_at DESC
    ''', (group_id,)).fetchall()
    
    return render_template('inventory.html', items=items)


@app.route('/shopping', methods=['GET', 'POST'])
def shopping():
    db = database.get_db()
    group_id = 1 # ※一旦グループID=1で固定してテストします

    if request.method == 'POST':
        # フォームから送信されたデータを受け取り、買うリスト（buy）としてDBに登録
        name = request.form.get('name')
        quantity = request.form.get('quantity', '')
        
        if name:
            db.execute('''
                INSERT INTO items (name, quantity, status, group_id)
                VALUES (?, ?, 'buy', ?)
            ''', (name, quantity, group_id))
            db.commit()
        return redirect(url_for('shopping'))

    # GETリクエスト時：DBから買うリストを取得して画面に渡す
    items = db.execute('''
        SELECT * FROM items 
        WHERE status = 'buy' AND group_id = ? 
        ORDER BY updated_at DESC
    ''', (group_id,)).fetchall()
    
    return render_template('shopping.html', items=items)


@app.route('/buy/<int:item_id>', methods=['POST'])
def buy_item(item_id):
    # 「買った！」ボタンを押したときの処理（buy -> stock へステータス変更）
    db = database.get_db()
    db.execute('''
        UPDATE items 
        SET status = 'stock', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (item_id,))
    db.commit()
    
    return redirect(url_for('shopping'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    # アイテムをデータベースから削除する処理
    db = database.get_db()
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()
    
    # 削除後、元のページ（在庫リスト or 買うリスト）に戻る
    return redirect(request.referrer or url_for('inventory'))


if __name__ == '__main__':
    app.run(debug=True)