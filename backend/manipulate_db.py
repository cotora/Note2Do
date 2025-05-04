import sqlite3
from datetime import datetime

from pydantic import BaseModel


class DB_Task(BaseModel):
    """
    データベースのタスク
    """

    id: int
    task_name: str
    start_date: datetime
    end_date: datetime
    result_time: int | None


class DuplicateTaskError(Exception):
    """
    重複タスクエラー
    """

    pass


def insert_task(
    task_name: str, start_date: datetime, end_date: datetime, result_time: int | None
):
    """
    タスクを挿入する

    Args:
        task_name (str): タスク名
        start_date (datetime): 開始日時
        end_date (datetime): 終了日時
        result_time (int|None): 結果時間

    Raises:
        DuplicateTaskError: 重複したタスクが存在する場合
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    try:
        # 挿入を試みる（データベースの一意制約により重複があればエラーになる）
        cursor.execute(
            """
            INSERT INTO tasks (task_name, start_date, end_date, result_time)
            VALUES (?, ?, ?, ?)
        """,
            (task_name, start_date, end_date, result_time),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # 一意制約違反によるエラーが発生した場合
        raise DuplicateTaskError(
            f"タスク '{task_name}' （{start_date}～{end_date}）はすでに存在しています。"
        )
    finally:
        cursor.close()
        conn.close()


def delete_task(task_id: int):
    """
    タスクを削除する

    Args:
        task_id (int): タスクID
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    cursor.close()
    conn.close()


def get_all_tasks() -> list[DB_Task]:
    """
    全てのタスクを取得する

    Returns:
        list[DB_Task]: 全てのタスク
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    tasks = [
        DB_Task(
            id=task[0],
            task_name=task[1],
            start_date=task[2],
            end_date=task[3],
            result_time=task[4],
        )
        for task in tasks
    ]

    cursor.close()
    conn.close()

    return tasks


if __name__ == "__main__":
    tasks = get_all_tasks()
    print(tasks)
