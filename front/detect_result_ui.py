import streamlit as st

# ページ全体のレイアウトを中央寄せに
st.set_page_config(layout="centered")

# タイトル
st.header("認識結果")

# 認識結果表示エリア
with st.container(border=True):

    # 日時表示
    st.text_input("", value="2025/05/10 10:00〜11:00", disabled=True)

    # タスク名と編集・削除ボタンを横に配置
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.write("タスク名")

    with col2:
        st.button(
            "編集",
            key="edit_button",
            type="secondary",
            help="このタスクを編集します",
        )

    with col3:
        st.button(
            "削除", key="delete_button", type="secondary", help="このタスクを削除します"
        )

# スペースを追加
st.write("")
st.write("")

# OKボタン
ok_col1, ok_col2, ok_col3 = st.columns([1, 1, 1])
with ok_col2:
    st.button("OK", type="primary", use_container_width=True)
