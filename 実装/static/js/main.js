document.addEventListener('DOMContentLoaded', () => {
    
    // 1. フォームの二重送信防止とUIフィードバック
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // このフォーム内にある送信ボタンを取得
            const submitBtn = this.querySelector('button[type="submit"]');
            
            if (submitBtn) {
                // すでに処理中の場合は送信をキャンセル（連打防止）
                if (submitBtn.classList.contains('is-loading')) {
                    e.preventDefault();
                    return;
                }
                
                // ボタンの見た目を半透明にし、クリックできない状態（CSSで設定済）にする
                submitBtn.classList.add('is-loading');
                
                // 押されたボタンのクラス（種類）に応じて、テキストを変更して反応を伝える
                if (submitBtn.classList.contains('btn-buy')) {
                    submitBtn.textContent = '処理中...';
                } else if (submitBtn.classList.contains('btn-delete')) {
                    submitBtn.textContent = '削除中...';
                } else {
                    // それ以外（在庫の「登録」や買うリストの「追加」ボタン）
                    submitBtn.textContent = '送信中...';
                }
            }
        });
    });

});