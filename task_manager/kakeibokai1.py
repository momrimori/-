import sqlite3

class TaskDB:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.init_db()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                is_done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

    def add_task(self, task_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (task) VALUES (?)",
                (task_name,)
            )

    def show_tasks(self,only_incomplete=False):
        with self.connect() as conn:
            cursor = conn.cursor()
            if only_incomplete:
                cursor.execute("SELECT * FROM tasks WHERE is_done=0 ORDER BY created_at DESC")
            else:
                cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            return cursor.fetchall()

    def complete_task(self, task_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET is_done = 1 WHERE id = ?",
                (task_id,)
            )

    def delete_task(self, task_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )

def main():
    db = TaskDB()

    while True:
        print("\n1. 追加")
        print("2. 一覧")
        print("3. 完了")
        print("4. 削除")
        print("5. 終了")

        choice = input("選択: ")

        if choice == "1":
            task = input("タスク名: ")
            db.add_task(task)

        elif choice == "2":
            print("1.全表示")
            print("2.未完了のみ")
            sub=input("選択： ")

            if sub=="2":
                tasks = db.show_tasks(True)
            else:
                tasks = db.show_tasks()

            for task in tasks:
                status = "✅" if task[2] else "❌"
                print(f"{task[0]} | {task[1]} | {status} | {task[3]}")

        elif choice == "3":
            task_id = int(input("完了するID: "))
            db.complete_task(task_id)

        elif choice == "4":
            task_id = int(input("削除するID: "))
            db.delete_task(task_id)

        elif choice == "5":
            break

if __name__ == "__main__":
    main()
    