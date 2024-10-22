from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database

# Создаем соединение с базой данных
DATABASE_URL = "sqlite:///main.db"
database = Database(DATABASE_URL)


# Определяем модель данных
class Note(BaseModel):
    title: str
    text: str


# Создаем экземпляр FastAPI
app = FastAPI()


# Подключаемся к базе данных при старте приложения
@app.on_event("startup")
async def startup():
    await database.connect()
    query = """CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                text TEXT NOT NULL
            );"""
    await database.execute(query=query)


# Отключаемся от базы данных при завершении работы
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Определяем маршрут для отображения заметок
@app.get("/")
async def show_notes():
    query = "SELECT * FROM notes"
    posts = await database.fetch_all(query=query)
    return posts


# Определяем маршрут для добавления заметки
@app.post("/note/")
async def add_note(note: Note):
    query = "INSERT INTO notes (title, text) VALUES (:title, :text)"
    values = {"title": note.title, "text": note.text}
    last_record_id = await database.execute(query=query, values=values)
    return {"message": "Note added successfully", "note_id": last_record_id}


# Определяем маршрут для обновления заметки
@app.put("/note/{note_id}")
async def update_note(note_id: int, note: Note):
    query = "SELECT id FROM notes WHERE id = :note_id"
    values = {"note_id": note_id}
    existing_note = await database.fetch_one(query=query, values=values)

    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    query = "UPDATE notes SET title = :title, text = :text WHERE id = :note_id"
    values = {"title": note.title, "text": note.text, "note_id": note_id}
    await database.execute(query=query, values=values)

    return {"message": "Note edited successfully"}


# Определяем маршрут для удаления заметки
@app.delete("/note/delete/{note_id}")
async def delete_note(note_id: int):
    query = "DELETE FROM notes WHERE id = :note_id"
    values = {"note_id": note_id}
    result = await database.execute(query=query, values=values)

    if result == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    return {"message": "Note deleted successfully"}
