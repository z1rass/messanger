from fastapi import FastAPI, HTTPException
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
    title: str
    text: str

# Создаем экземпляр FastAPI
app = FastAPI()

# Определяем маршрут для отображения заметок
@app.get("/")
async def show_notes():
    c.execute("SELECT * FROM notes")
    posts = c.fetchall()
    return posts

# Определяем маршрут для добавления заметки
@app.post("/note/")
async def add_note(note: Note):
    # Используем правильное имя таблицы и передаем значение в качестве параметра
    c.execute("INSERT INTO notes (title, text) VALUES (?, ?)", (note.title, note.text,))
    con.commit()
    idshka = c.lastrowid

    return {"message": "Note added successfully", "note_id": idshka}


@app.put("/note/{note_id}")
async def update_note(note_id: int, note: Note):
    # Проверяем, существует ли заметка с данным ID
    c.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
    existing_note = c.fetchone()

    if existing_note is None:
        return {"error": "Note not found"}, 404

    # Обновляем заметку, если она существует
    c.execute("UPDATE notes SET title = ?, text = ? WHERE id = ?", (note.title, note.text, note_id))
    con.commit()

    return {"message": "Note edited successfully"}


@app.delete("/note/delete/{note_id}")
async def add_note(note_id: int):
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    con.commit()
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}