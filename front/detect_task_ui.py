import streamlit as st
from detect_result_ui import detect_result_ui

def detect_task_ui():
    """
    タスクを自動で認識するUI
    """

    # 入力テキスト管理
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""

    # ページ状態管理
    if "page" not in st.session_state:
        st.session_state["page"] = "input"

    # ページ全体のレイアウトを中央寄せに
    #st.set_page_config(layout="centered")

    # 入力ページの表示
    if st.session_state["page"] == "input":
        # タイトル
        st.title("タスクを自動で認識")

        # テキストエリア
        input_text = st.text_area(
            label="文章を入力してください...",
            value=st.session_state["input_text"],
            key="input_text_area",
            height=150,
        )

        # スペースを追加
        st.write("")
        st.write("")

        # 完了ボタンを目立たせる
        st.subheader("✅ 入力が完了したら下のボタンをクリック")

        # 完了ボタン（大きめに表示）
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            if st.button(
                "📝 タスクを認識する 📝",
                key="submit_button",
                use_container_width=True,
            ):
                if input_text:
                    # ページ状態を結果表示に変更
                    st.session_state["page"] = "result"
                    st.session_state["input_text"] = input_text
                    st.rerun()  # ページを再読み込み
                else:
                    st.error("文章を入力してください")

    # 結果ページの表示
    elif st.session_state["page"] == "result":
        # 結果UIを表示
        detect_result_ui(st.session_state["input_text"])
        # 戻るボタン
        if st.button("入力画面に戻る"):
            st.session_state["page"] = "input"
            st.session_state.pop("tasks")
            st.rerun()

# サイドバー関連
## 関数定義
def logDebug(msg:str):
    st.session_state.log_count+=1
    st.session_state.debug_message+=f"{st.session_state.log_count}:{msg}\n" #ユーザー入力記録

## 初期化
### デバッグ用メッセージ関連変数宣言
if "debug_message" not in st.session_state:
    st.session_state.debug_message=""
if "log_count" not in st.session_state:
    st.session_state.log_count=0

if "side_bar_id" not in st.session_state:
    st.session_state.side_bar_id=1 # サイドバーのどのタブを表示するか_初期はメインメニューで    
    # 0: デバッグログ確認
    # 1: メインメニューサイドバー

## メイン部分
with st.sidebar:
    #サイドバーの表示タブ選択ボタン
    option=st.selectbox(
        "Select the menu in this side bar."
        ,["Main","Debug Log"]
    )
    if option=="Debug Log":
        st.session_state.side_bar_id=0
    elif option=="Main":
        st.session_state.side_bar_id=1

    if st.session_state.side_bar_id==0:#デバッグ用サイドバー表示
        st.markdown("### Debug Log")
        debug_str="" #デバッグ記録出力用文字列
        for id,msg in enumerate(st.session_state.debug_message):
            debug_str+=f"number:{id}:{msg}\n"
        st.text_area("content",st.session_state.debug_message)
    elif st.session_state.side_bar_id==1:#メインサイドバー表示
        st.markdown("### メニュー")
        if st.button("① カレンダー"):
            logDebug("カレンダーボタン押下")#ユーザー入力記録
            st.session_state.page="MainMenu"#カレンダー画面の呼び出し
            st.switch_page("MainMenu.py")
            pass
        if st.button("② 今日のタスク"):
            logDebug("今日のタスクボタン押下")#ユーザー入力記録
            st.session_state.page="Today_schedule"#今日のタスク画面の呼び出し
            st.switch_page("Today_schedule.py")
            pass
        if st.button("③ 音声認識タスク登録"):
            logDebug("音声認識タスク登録")#ユーザー入力記録
            st.session_state.page="input"#音声認識画面の呼び出し
            st.switch_page("detect_task_ui.py")
            pass

if __name__ == "__main__":
    detect_task_ui()
