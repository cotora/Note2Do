import os
import sys

import streamlit as st

# パスを追加して親ディレクトリのモジュールをインポートできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.extract_task import extract_task
from backend.manipulate_db import DuplicateTaskError, insert_task


def detect_result_ui(input_text: str):
    """
    認識結果を表示するUI

    Args:
        input_text (str): 認識結果のテキスト
    """
    # ページ全体のレイアウトを中央寄せに
    # set_page_configは親ページで設定する必要があるため削除

    # タスク状態の管理
    if "tasks" not in st.session_state:
        # 初回表示時にタスクを抽出
        st.session_state["tasks"] = extract_task(input_text)

    # タイトル
    st.header("認識結果")

    # タスクの表示
    if len(st.session_state["tasks"]) == 0:
        st.error("タスク情報が見つかりませんでした")
    else:
        st.success(f"{len(st.session_state['tasks'])}件のタスクが見つかりました")

        # 各タスクを表示
        for i, task in enumerate(st.session_state["tasks"]):
            with st.container(border=True):
                st.subheader(f"タスク {i + 1}")

                # 日時表示
                st.caption("日時")
                date_col, start_time_col, time_separator_col, end_time_col = st.columns(
                    [2, 1, 0.2, 1]
                )

                # タスクから日付と時間を取得
                task_date = task.start_date.date()
                task_start_time = task.start_date.time()
                task_end_time = task.end_date.time()

                with date_col:
                    st.date_input(
                        f"日付_{i}",
                        value=task_date,
                        key=f"date_{i}",
                        label_visibility="collapsed",
                    )

                with start_time_col:
                    st.time_input(
                        f"開始時間_{i}",
                        value=task_start_time,
                        key=f"start_time_{i}",
                        label_visibility="collapsed",
                    )

                with time_separator_col:
                    st.write("～")

                with end_time_col:
                    st.time_input(
                        f"終了時間_{i}",
                        value=task_end_time,
                        key=f"end_time_{i}",
                        label_visibility="collapsed",
                    )

                # タスク名入力エリア
                st.caption("タスク名")
                st.text_input(
                    f"タスク名_{i}",
                    value=task.task_name,
                    key=f"task_name_{i}",
                    label_visibility="collapsed",
                )

                # 削除ボタン
                delete_col1, delete_col2, delete_col3 = st.columns([1, 1, 1])
                with delete_col2:
                    if st.button(
                        "削除",
                        key=f"delete_button_{i}",
                        type="secondary",
                        help="このタスクを削除します",
                        use_container_width=True,
                    ):
                        st.session_state["tasks"].pop(i)
                        st.rerun()

        # スペースを追加
        st.write("")
        st.write("")

        # OKボタン
        ok_col1, ok_col2, ok_col3 = st.columns([1, 1, 1])
        with ok_col2:
            if st.button("OK", type="primary", use_container_width=True):
                # タスクをデータベースに保存
                success_count = 0
                duplicate_count = 0

                for task in st.session_state["tasks"]:
                    try:
                        insert_task(
                            task.task_name, task.start_date, task.end_date, None
                        )
                        success_count += 1
                    except DuplicateTaskError as e:
                        duplicate_count += 1
                        st.warning(str(e))

                if success_count > 0:
                    st.success(f"{success_count}件のタスクを保存しました")

                if duplicate_count > 0:
                    st.warning(
                        f"{duplicate_count}件のタスクは重複のため保存されませんでした"
                    )


if __name__ == "__main__":
    detect_result_ui(
        "ポスターセッションは5月15日（木）18:00〜20:00に学内カフェテリアにて実施予定です。"
    )
