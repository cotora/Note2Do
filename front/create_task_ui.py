from datetime import time

import streamlit as st


def create_task_ui():
    """
    タスクを手動で作成するUI
    """
    # ページ全体のレイアウトを中央寄せに
    st.set_page_config(layout="centered")

    # タイトル（非表示）
    # st.title("タスク登録")

    # タスク情報入力エリア
    # タスク名入力
    st.text_input("タスク名を入力：", key="task_name")

    # スペースを追加
    st.write("")
    st.write("")

    # 開始時刻と終了時刻を横に並べる
    col1, col2 = st.columns(2)

    with col1:
        # 開始時刻入力
        start_time = st.time_input(
            "タスクの開始時刻を入力：",
            value=time(9, 0),
            key="start_time",
            step=300,  # 5分単位
        )

    with col2:
        # 終了時刻入力
        end_time = st.time_input(
            "タスクの終了時刻を入力：",
            value=time(10, 0),
            key="end_time",
            step=300,  # 5分単位
        )

    # スペースを追加
    st.write("")
    st.write("")
    st.write("")

    # タスク作成ボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("タスク作成", use_container_width=True, type="primary"):
            # タスク名のバリデーション
            if not st.session_state.task_name:
                st.error("タスク名を入力してください")
            # 時刻のバリデーション
            elif start_time >= end_time:
                st.error("終了時刻は開始時刻より後に設定してください")
            else:
                # データの保存処理（ここでは成功メッセージのみ表示）
                st.success("タスクが作成されました")

                # 実際のデータ保存処理はここに実装
                # 例: データベースへの保存、APIへのデータ送信など


if __name__ == "__main__":
    create_task_ui()
