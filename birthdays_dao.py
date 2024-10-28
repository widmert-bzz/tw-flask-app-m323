import sqlite3
from birthday import Birthday

class BirthdaysDao:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''DROP TABLE IF EXISTS todo_items''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS todo_items (
                item_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id))'''
        )
        self.conn.commit()

    def add_item(self, birthday_item):
        self.cursor.execute("INSERT INTO todo_items (user_id, name, date) VALUES (?, ?, ?)",
                            (birthday_item.user_id, birthday_item.name, birthday_item.date))
        self.conn.commit()

    def get_item(self, item_id, user_id):
        self.cursor.execute("SELECT * FROM todo_items WHERE item_id = ? AND user_id = ?", (item_id, user_id))
        row = self.cursor.fetchone()
        if row:
            return Birthday(row[0], row[1], row[2], row[3])
        return None

    def get_all_items(self, user_id):
        self.cursor.execute("SELECT * FROM todo_items WHERE user_id = ?", (user_id,))
        rows = self.cursor.fetchall()
        birthday_items = [Birthday(row[0], row[1], row[2], row[3]) for row in rows]
        return birthday_items

    def update_item(self, birthday_item):
        self.cursor.execute("UPDATE todo_items SET name = ?, date = ? WHERE item_id = ? AND user_id = ?",
                            (birthday_item.name, birthday_item.date, birthday_item.item_id, birthday_item.user_id))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_item(self, item_id, user_id):
        self.cursor.execute("DELETE FROM todo_items WHERE item_id = ? AND user_id = ?", (item_id, user_id))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()