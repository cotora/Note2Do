import sqlite3
from datetime import date, datetime

from pydantic import BaseModel


# SQLite日時アダプターの登録
def adapt_datetime(dt):
    return dt.isoformat()


def convert_datetime(value):
    try:
        return datetime.fromisoformat(value.decode())
    except (ValueError, AttributeError):
        return value


# アダプターを登録
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)


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
    conn = sqlite3.connect("tasks.db", detect_types=sqlite3.PARSE_DECLTYPES)
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
    conn = sqlite3.connect("tasks.db", detect_types=sqlite3.PARSE_DECLTYPES)
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
    conn = sqlite3.connect("tasks.db", detect_types=sqlite3.PARSE_DECLTYPES)
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


def get_task_by_date(target_date: date) -> list[DB_Task]:
    """
    指定された日付の日が開始時刻の日と一致するタスクを取得する

    Args:
        target_date (date): 日付

    Returns:
        list[DB_Task]: 指定された日付のタスク
    """
    conn = sqlite3.connect("tasks.db", detect_types=sqlite3.PARSE_DECLTYPES)

    # 日付の変換を適切に行うための設定
    conn.execute("PRAGMA foreign_keys = ON")

    cursor = conn.cursor()

    # 指定日の開始と終了（00:00:00から23:59:59まで）
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())

    # 開始日時が指定された日の範囲内にあるタスクを検索
    cursor.execute(
        """
        SELECT id, task_name, start_date, end_date, result_time
        FROM tasks
        WHERE start_date >= ? AND start_date < ?
        ORDER BY start_date ASC
    """,
        (start_of_day, end_of_day),
    )

    tasks_data = cursor.fetchall()

    # タスクオブジェクトに変換
    tasks = []
    for task_data in tasks_data:
        tasks.append(
            DB_Task(
                id=task_data[0],
                task_name=task_data[1],
                start_date=task_data[2],
                end_date=task_data[3],
                result_time=task_data[4],
            )
        )

    cursor.close()
    conn.close()

    return tasks


if __name__ == "__main__":
    tasks = get_all_tasks()
    print(tasks)

    # 今日のタスクを取得する例
    insert_task(
        task_name="test",
        start_date=datetime.now(),
        end_date=datetime.now(),
        result_time=100,
    )
    today_tasks = get_task_by_date(date.today())
    print(f"今日のタスク: {today_tasks}")
