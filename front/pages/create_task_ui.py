import datetime
import os
import sys
from datetime import time

import streamlit as st

# パスを追加して親ディレクトリのモジュールをインポートできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.manipulate_db import DuplicateTaskError, insert_task


def create_task_ui(cur_date: datetime.date):
    """
    タスクを手動で作成するUI

    Args:
        cur_date (datetime.date): 現在の日付
    """
    # ページ全体のレイアウトを中央寄せに
    # st.set_page_config(layout="centered")

    # タイトル（非表示）
    # st.title("タスク登録")

    # タスク情報入力エリア
    # タスク名入力
    st.text_input("タスク名を入力：", key="task_name")

    # スペースを追加
    st.write("")
    st.write("")

    # 榮留により追加
    st.write(
        f"{st.session_state.selected_year}年{st.session_state.selected_month}月{st.session_state.selected_day}日"
    )

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
                try:
                    # 現在選択されている日付と入力された時間を組み合わせる
                    task_date = datetime.date(
                        st.session_state.selected_year,
                        st.session_state.selected_month,
                        st.session_state.selected_day,
                    )

                    # 開始時刻と終了時刻を作成
                    start_datetime = datetime.datetime.combine(task_date, start_time)
                    end_datetime = datetime.datetime.combine(task_date, end_time)

                    # データベースにタスクを登録
                    insert_task(
                        task_name=st.session_state.task_name,
                        start_date=start_datetime,
                        end_date=end_datetime,
                        result_time=None,
                    )

                    # 成功メッセージを表示
                    st.success("タスクが作成されました")

                    # 入力フォームをクリア
                    st.session_state.task_name = ""

                except DuplicateTaskError as e:
                    # 重複エラーの場合
                    st.error(f"タスク登録エラー: {e}")
                except Exception as e:
                    # その他のエラー
                    st.error(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    create_task_ui(datetime.datetime.now())
