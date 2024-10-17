from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
import requests

kb = KeyBindings()

@kb.add('c-q')
def exit(event):
    app.exit()
    if (len(buffer1.text) > 0):
        requests.post("http://127.0.0.1:8000/user", json={'text' : buffer1.text})


@kb.add('c-s')
def save(event):
    text = buffer1.text

# Функция для переключения фокуса между окнами
@kb.add('c-n')
def switch_focus(event):
    get_app().layout.focus_next()

buffer1 = Buffer()  # Editable buffer.

root_container = VSplit([
    # One window that holds the BufferControl with the default buffer on
    # the left.
    Window(content=BufferControl(buffer=buffer1))
])

layout = Layout(root_container)

app = Application(layout=layout, full_screen=True, key_bindings=kb)

app.run()  # You won't be able to Exit this app
