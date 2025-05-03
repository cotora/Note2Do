import datetime

import streamlit as st

# ページ全体のレイアウトを中央寄せに
st.set_page_config(layout="centered")

# タイトル
st.header("認識結果")

# 認識結果表示エリア
with st.container(border=True):
    # 日時表示
    st.caption("日時")
    date_col, start_time_col, time_separator_col, end_time_col = st.columns(
        [2, 1, 0.2, 1]
    )

    with date_col:
        st.date_input(
            "日付",
            value=datetime.date(2025, 5, 10),
            label_visibility="collapsed",
        )

    with start_time_col:
        st.time_input(
            "開始時間",
            value=datetime.time(10, 0),
            label_visibility="collapsed",
        )

    with time_separator_col:
        st.write("～")

    with end_time_col:
        st.time_input(
            "終了時間",
            value=datetime.time(11, 0),
            label_visibility="collapsed",
        )

    # タスク名入力エリア
    st.caption("タスク名")
    task_name = st.text_input(
        "タスク名", value="ミーティング", label_visibility="collapsed"
    )

    # 削除ボタン
    delete_col1, delete_col2, delete_col3 = st.columns([1, 1, 1])
    with delete_col2:
        st.button(
            "削除",
            key="delete_button",
            type="secondary",
            help="このタスクを削除します",
            use_container_width=True,
        )

# スペースを追加
st.write("")
st.write("")

# OKボタン
ok_col1, ok_col2, ok_col3 = st.columns([1, 1, 1])
with ok_col2:
    st.button("OK", type="primary", use_container_width=True)
