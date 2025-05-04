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


if __name__ == "__main__":
    detect_task_ui()
