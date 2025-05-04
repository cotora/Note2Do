import sqlite3


def create_db():
    """
    データベースを作成する
    """
    conn = sqlite3.connect("tasks.db")

    # テーブルの作成
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            result_time INTEGER,
            UNIQUE(task_name, start_date, end_date)
        )
    """
    )

    # テーブルの作成
    conn.commit()

    # テーブルの作成
    conn.close()


if __name__ == "__main__":
    create_db()
