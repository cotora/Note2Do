root
├front:UI関係のコードを管理
└backend:内部処理のコードを管理

・フレームワーク
streamlitを使う方針

・Gitコマンドメモ
├git clone <url>:リモートリポジトリの内容をローカルにコピー
│
├git add <ファイル名>:ローカルのファイル単位の変更内容を仮で保存
│
├git commit -m "メッセージ"：git addで貯めた変更内容をメッセージ付きで実際に保存
│
├git push origin main:コミットの変更内容をリモートリポジトリに反映
│
└git pull origin main:リモートリポジトリの変更内容をローカルに反映

・PowerShell コマンドメモ
・New-Item -Type File パス名
・Move-Item -Pass 対象ファイルパス -Destination 目的地ファイルパス名

・Streamlit 関連
st.columns(cols):cols列だけstを取得でき，ボタンの行列を作成可能
st.rerun():再読み込み

・設計メモ
MainMenu.pyが呼び出される為，if文を駆使し，関数化したページを呼び出して制御
    _ページ遷移管理：st.session.pageの値で管理
        "MainMenu":メインメニュー
        "input_hand":create_task_ui.pyへ
        "input":detect_task_ui.pyへ
st.set_page_configは最初の1回しか呼び出せないので，MainMenu.pyのみ呼び出すように変更

・WSL+GitHub連携
_GHコマンドを見てみる．

・ワークシートURL
https://docs.google.com/presentation/d/1YLFH4EMAZI_F1faT0MmnIJIUzeZRPjItbXIDsMSNc88/edit?usp=drive_link

・ひな形コード生成AI
https://claude.ai/
https://v0.dev/chat