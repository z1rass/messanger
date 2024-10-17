from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# Создаем соединение с базой данных и создаем курсор
con = sqlite3.connect("main.db")
c = con.cursor()

# Создаем таблицу notes, если она не существует
sql = """CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL);"""
c.execute(sql)

# Определяем модель данных
class Note(BaseModel):
    text: str

# Создаем экземпляр FastAPI
app = FastAPI()

# Определяем маршрут для отображения заметок
@app.get("/")
async def show_notes():
    c.execute("SELECT * FROM users")
    return c.fetchall()

# Определяем маршрут для добавления заметки
@app.post("/user/")
async def add_note(note: Note):
    # Используем правильное имя таблицы и передаем значение в качестве параметра
    c.execute("INSERT INTO users (text) VALUES (?)", (note.text,))
    con.commit()
    return {"message": "Note added successfully"}