import os
import sys
from datetime import datetime

import streamlit as st

# パスを追加して親ディレクトリのモジュールをインポートできるようにする
sys.path.insert(
    0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
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
    if "tasks_s" not in st.session_state:
        # 初回表示時にタスクを抽出
        st.session_state["tasks_s"] = extract_task(input_text)
        st.session_state["tasks_s"] = [task for task in st.session_state["tasks_s"] if task.start_date.date() == task.end_date.date() and task.start_date.time() <= task.end_date.time()]

    # 入力値の変更をタスクに反映する関数
    def update_task_name(idx):
        """
        タスク名を変更する関数

        Args:
            idx (int): タスクのインデックス
        """
        st.session_state["tasks_s"][idx].task_name = st.session_state[f"task_name_{idx}"]

    def update_task_date(idx):
        """
        日付が変更されたら開始日時と終了日時の日付部分を更新

        Args:
            idx (int): タスクのインデックス
        """
        # 日付が変更されたら開始日時と終了日時の日付部分を更新
        old_start = st.session_state["tasks_s"][idx].start_date
        old_end = st.session_state["tasks_s"][idx].end_date
        # 新しい日付と元の時間を組み合わせる
        new_date = st.session_state[f"date_{idx}"]
        st.session_state["tasks_s"][idx].start_date = datetime.combine(
            new_date, old_start.time()
        )
        st.session_state["tasks_s"][idx].end_date = datetime.combine(
            new_date, old_end.time()
        )

    def update_task_start_time(idx):
        """
        開始時間が変更されたら開始日時の時間部分を更新

        Args:
            idx (int): タスクのインデックス
        """
        # 開始時間が変更されたら開始日時の時間部分を更新
        old_start = st.session_state["tasks_s"][idx].start_date
        # 元の日付と新しい時間を組み合わせる
        new_time = st.session_state[f"start_time_{idx}"]
        new_start_datetime = datetime.combine(old_start.date(), new_time)

        # 終了時刻より後になっていないかチェック
        end_datetime = st.session_state["tasks_s"][idx].end_date
        if new_start_datetime > end_datetime:
            # エラーメッセージを表示
            st.session_state[f"start_time_{idx}"] = old_start.time()
        else:
            # 有効な時間なので更新
            st.session_state["tasks_s"][idx].start_date = new_start_datetime

    def update_task_end_time(idx):
        """
        終了時間が変更されたら終了日時の時間部分を更新

        Args:
            idx (int): タスクのインデックス
        """
        # 終了時間が変更されたら終了日時の時間部分を更新
        old_end = st.session_state["tasks_s"][idx].end_date
        # 元の日付と新しい時間を組み合わせる
        new_time = st.session_state[f"end_time_{idx}"]
        new_end_datetime = datetime.combine(old_end.date(), new_time)

        # 開始時刻より前になっていないかチェック
        start_datetime = st.session_state["tasks_s"][idx].start_date
        if new_end_datetime < start_datetime:
            st.session_state[f"end_time_{idx}"] = old_end.time()
        else:
            # 有効な値なので更新
            st.session_state["tasks_s"][idx].end_date = new_end_datetime

    # タイトル
    st.header("認識結果")

    # タスクの表示
    if len(st.session_state["tasks_s"]) == 0:
        st.error("タスク情報が見つかりませんでした")
    else:
        st.success(f"{len(st.session_state['tasks_s'])}件のタスクが見つかりました")

        # 各タスクを表示
        for i, task in enumerate(st.session_state["tasks_s"]):
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
                    _ = st.date_input(
                        f"日付_{i}",
                        value=task_date,
                        key=f"date_{i}",
                        label_visibility="collapsed",
                        on_change=update_task_date,
                        args=(i,),
                    )

                with start_time_col:
                    _ = st.time_input(
                        f"開始時間_{i}",
                        value=task_start_time,
                        key=f"start_time_{i}",
                        label_visibility="collapsed",
                        on_change=update_task_start_time,
                        args=(i,),
                    )

                with time_separator_col:
                    st.write("～")

                with end_time_col:
                    _ = st.time_input(
                        f"終了時間_{i}",
                        value=task_end_time,
                        key=f"end_time_{i}",
                        label_visibility="collapsed",
                        on_change=update_task_end_time,
                        args=(i,),
                    )

                # タスク名入力エリア
                st.caption("タスク名")
                _ = st.text_input(
                    f"タスク名_{i}",
                    value=task.task_name,
                    key=f"task_name_{i}",
                    label_visibility="collapsed",
                    on_change=update_task_name,
                    args=(i,),
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
                        st.session_state["tasks_s"].pop(i)
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

                for task in st.session_state["tasks_s"]:
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