import sqlite3
from datetime import datetime
import random

# Подключение к БД
conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type TEXT,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()


# Добавление пользователей
def create_user(name, email):
    cursor.execute(
        "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
        (name, email, datetime.now().isoformat())
    )
    conn.commit()


# Логирование событий
def log_event(user_id, event_type):
    cursor.execute(
        "INSERT INTO events (user_id, event_type, created_at) VALUES (?, ?, ?)",
        (user_id, event_type, datetime.now().isoformat())
    )
    conn.commit()


# Генерация тестовых данных
users = [
    ("Alice", "alice@mail.com"),
    ("Bob", "bob@mail.com"),
    ("Charlie", "charlie@mail.com"),
]

for name, email in users:
    create_user(name, email)

for _ in range(20):
    user_id = random.randint(1, 3)
    event = random.choice(["login", "click", "purchase"])
    log_event(user_id, event)


# 📊 Аналитика

print("\n🔥 Самые активные пользователи:")
cursor.execute("""
SELECT users.name, COUNT(events.id) as events_count
FROM events
JOIN users ON users.id = events.user_id
GROUP BY users.id
ORDER BY events_count DESC
""")

for row in cursor.fetchall():
    print(row)


print("\n📈 Количество событий по типу:")
cursor.execute("""
SELECT event_type, COUNT(*)
FROM events
GROUP BY event_type
""")

for row in cursor.fetchall():
    print(row)


conn.close()
