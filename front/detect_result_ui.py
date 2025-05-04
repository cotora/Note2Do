import os
import sys

import streamlit as st

# パスを追加して親ディレクトリのモジュールをインポートできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.extract_task import extract_task


def detect_result_ui(input_text: str):
    """
    認識結果を表示するUI

    Args:
        input_text (str): 認識結果のテキスト
    """
    # ページ全体のレイアウトを中央寄せに
    # set_page_configは親ページで設定する必要があるため削除

    # タイトル
    st.header("認識結果")

    # 認識結果の抽出
    tasks = extract_task(input_text)
    if len(tasks) == 0:
        st.error("タスク情報が見つかりませんでした")
    else:
        st.success(f"{len(tasks)}件のタスクが見つかりました")

        # 各タスクを表示
        for i, task in enumerate(tasks):
            with st.container(border=True):
                st.subheader(f"タスク {i + 1}")

                # 日時表示
                st.caption("日時")
                date_col, start_time_col, time_separator_col, end_time_col = st.columns(
                    [2, 1, 0.2, 1]
                )

                # タスクから日付と時間を取得
                task_date = task.start_time.date()
                task_start_time = task.start_time.time()
                task_end_time = task.end_time.time()

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
                    st.button(
                        "削除",
                        key=f"delete_button_{i}",
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


if __name__ == "__main__":
    detect_result_ui("ポスターセッションは5月15日（木）18:00〜20:00に学内カフェテリアにて実施予定です。")
