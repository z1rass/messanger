from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
import requests
from prompt_toolkit.shortcuts import radiolist_dialog

kb = KeyBindings()
id = 0


async def main_menu():
    posts = requests.get("http://127.0.0.1:8000/").json()
    print(posts)
    if not posts:  # Проверяем, пуст ли список
        posts = [[-1, "No data", "No data"]]  # Добавляем фиктивную запись
    result = await radiolist_dialog(
        title="Main Menu",
        text="Выберите один из вариантов:",
        values=[(str(i[0]), str(i[2])) for i in posts
        ],
    ).run_async()
    buffer1.text = ''
    for i in posts:
        if str(i[0]) == str(result):
            global id
            id = str(result)
            buffer1.text = i[1]
            app.reset()


async def action_menu():
    result = await radiolist_dialog(
        title="Action Menu",
        text="Choose action:",
        values=[("delete", "Delete")],
    ).run_async()
    if result == "delete":
        requests.delete(f"https://messanger-u8ic.onrender.com/note/delete/{id}")
        buffer1.text = ""
        app.reset()

def get_title():
    try:
        title = buffer1.text.split("\n")[0]
        return title
    except Exception:
        print("Error, cant see title")


@kb.add('c-q')
def exit(event):
    title = get_title()
    if len(buffer1.text) > 0 and buffer1.text != "#FIRST LINE ALWAYS TITLE, DELETE THIS LINE":
        requests.post("https://messanger-u8ic.onrender.com/note", json={'title': title, 'text': buffer1.text})
    app.exit()

@kb.add('c-f')
def menu(event):
    get_app().create_background_task(main_menu())

@kb.add('c-s')
def save_note(event):
    title = get_title()
    if len(buffer1.text) > 0 and buffer1.text != "#FIRST LINE ALWAYS TITLE, DELETE THIS LINE":
        requests.post("https://messanger-u8ic.onrender.com/note/", json={'title': title, 'text': buffer1.text})


@kb.add("c-i")
def a_menu(event):
    get_app().create_background_task(action_menu())


@kb.add('enter')
def insert_new_line(event):
    buffer1.insert_text('\n')

# Функция для переключения фокуса между окнами
@kb.add('c-n')
def switch_focus(event):
    get_app().layout.focus_next()

buffer1 = Buffer()  # Editable buffer.
buffer1.insert_text("#FIRST LINE ALWAYS TITLE, DELETE THIS LINE")

root_container = VSplit([
    # One window that holds the BufferControl with the default buffer on
    # the left.

    Window(content=BufferControl(buffer=buffer1))
])

layout = Layout(root_container)

app = Application(layout=layout, full_screen=True, key_bindings=kb)
if __name__ == '__main__':
    app.run()
