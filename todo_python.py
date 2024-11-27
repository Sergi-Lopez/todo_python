from tkinter import *
import sqlite3
import bcrypt

# Configuración inicial de la ventana
root = Tk()
root.title("Simple todo list with Login")
root.geometry('500x500')

# Conexión a la base de datos
conn = sqlite3.connect("todo.db")
c = conn.cursor()

# Tablas necesarias: usuarios y tareas

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    completed BOOLEAN NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")
conn.commit()

# Variables globales
current_user_id = None

# Función para encriptar contraseñas
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Función para verificar contraseñas
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Función para renderizar tareas
def render_todos():
    global current_user_id
    if current_user_id is None:
        return

    rows = c.execute("SELECT * FROM todo WHERE user_id = ?", (current_user_id,)).fetchall()

    for widget in frame.winfo_children():
        widget.destroy()
    
    for i, row in enumerate(rows):
        id = row[0]
        completed = row[3]
        description = row[2]
        color = '#2bd450' if completed else '#2822dd'
        l = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command=complete(id))
        l.grid(row=i, column=0, sticky='w')
        btn = Button(frame, text="Delete task", command=remove(id))
        btn.grid(row=i, column=1)
        l.select() if completed else l.deselect()

# Función para agregar tareas
def addTodo():
    global current_user_id
    if current_user_id is None:
        return

    todo = e.get()
    if todo:
        c.execute("""
        INSERT INTO todo (description, completed, user_id) VALUES (?, ?, ?)
        """, (todo, False, current_user_id))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass

# Funciones para completar y eliminar tareas
def complete(id):
    def _complete():
        todo = c.execute("SELECT * FROM todo WHERE id = ?", (id,)).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos()
    return _complete

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id,))
        conn.commit()
        render_todos()
    return _remove

# Función para iniciar sesión
def login():
    global current_user_id
    username = username_entry.get()
    password = password_entry.get()

    user = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user and verify_password(password, user[2]):
        current_user_id = user[0]
        login_frame.pack_forget()
        todo_frame.pack(fill='both', expand=1)
        render_todos()
    else:
        login_error_label.config(text="Invalid username or password", fg="red")

# Función para registrarse
def register():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        hashed_password = hash_password(password)
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            login_error_label.config(text="User registered successfully", fg="green")
        except sqlite3.IntegrityError:
            login_error_label.config(text="Username already exists", fg="red")
    else:
        login_error_label.config(text="Please fill all fields", fg="red")

# Interfaz de usuario para el login
login_frame = Frame(root)
login_frame.pack(fill='both', expand=1)

Label(login_frame, text="Username").pack(pady=5)
username_entry = Entry(login_frame)
username_entry.pack(pady=5)

Label(login_frame, text="Password").pack(pady=5)
password_entry = Entry(login_frame, show='*')
password_entry.pack(pady=5)

login_error_label = Label(login_frame, text="")
login_error_label.pack(pady=5)

Button(login_frame, text="Login", command=login).pack(pady=5)
Button(login_frame, text="Register", command=register).pack(pady=5)

# Interfaz de usuario para las tareas
todo_frame = Frame(root)

l = Label(todo_frame, text="Task")
l.grid(row=0, column=0)

e = Entry(todo_frame, width=40)
e.grid(row=0, column=1)

btn = Button(todo_frame, text="Add task", command=addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(todo_frame, text="My tasks", padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

e.focus()

root.mainloop()
