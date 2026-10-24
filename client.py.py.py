from customtkinter import *
from socket import *
from threading import Thread
from tkinter import messagebox

# --- НАСТРОЙКА ОКНА ---
window = CTk()
window.title("Ctk Chat")
window.minsize(1000, 600)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=2)
window.grid_rowconfigure(0, weight=1)

nickname = "Користувач"
avatar_window = None
is_validating = False  # Флаг против дублирования окон ошибок

# --- СЕТЕВАЯ ЛОГИКА ---
client_socket = socket(AF_INET, SOCK_STREAM)


def connect_to_server():
    try:
        client_socket.connect(("127.0.0.1", 7070))
        hread = Thread(target=recv_message, daemon=True)
        hread.start()
    except Exception as e:
        messagebox.showerror("Помилка підключення", f"Не вдалося підключитися до сервера:\n{e}")


def ask_nickname():
    global nickname
    input_dialog = CTkInputDialog(text="Введіть свій нікнейм:", title="Авторизація")
    choice = input_dialog.get_input()
    if choice and choice.strip():
        nickname = choice.strip()
    username_label.configure(text=nickname)


def send_msg():
    message = h.get()
    if message:
        try:
            full_message = f"{nickname}: {message}"
            client_socket.send(full_message.encode())

            g.configure(state="normal")
            g.insert("end", f"Ви: {message}\n")
            g.configure(state="disabled")
            g.see("end")

            h.delete(0, "end")
        except Exception as e:
            print(e)


def recv_message():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                g.configure(state="normal")
                g.insert("end", f"{message}\n")
                g.configure(state="disabled")
                g.see("end")
        except:
            break


# --- ВАЛИДАЦИЯ ПРОФИЛЯ ---
def check_game(event):
    global is_validating
    if is_validating:
        return

    text = game_entry.get().strip()
    if text:
        if not ("дота" in text.lower() or "dota" in text.lower()):
            is_validating = True
            messagebox.showerror("Помилка!", "Невірний вибір! Дозволена тільки Дота 👿")
            game_entry.delete(0, "end")
            is_validating = False


def check_age(event):
    global is_validating
    if is_validating:
        return

    text = age_entry.get().strip()
    if text:
        if not text.isdigit() or int(text) < 0 or int(text) > 120:
            is_validating = True
            messagebox.showerror("Помилка!", "Некоректний вік! Введіть число від 0 до 120.")
            age_entry.delete(0, "end")
            is_validating = False


# --- ИЗМЕНЕНИЕ ТЕМЫ ОФОРМЛЕННЯ ---
def toggle_theme():
    if theme_switch.get() == 1:
        set_appearance_mode("light")
    else:
        set_appearance_mode("dark")


# --- БЕЗОПАСНАЯ ОЧИСТКА ОКНА ЧАТА ПРИ ДВОЙНОМ КЛИКЕ ---
def clear_chat_history(event):
    try:
        g.configure(state="normal")
        g.delete("1.0", "end")
        g.configure(state="disabled")
    except Exception as e:
        print(e)


# --- ЛОГИКА СМЕНЫ АВАТАРОК (БЕЗ РИСОВАНИЯ) ---
def change_avatar(chosen_emoji):
    avatar.configure(text=chosen_emoji)
    if avatar_window:
        avatar_window.destroy()


def open_avatar_selector():
    global avatar_window
    avatar_window = CTkToplevel(window)
    avatar_window.title("Вибір аватарки")
    avatar_window.geometry("300x150")
    avatar_window.resizable(False, False)
    avatar_window.attributes("-topmost", True)

    title = CTkLabel(avatar_window, text="Оберіть свій смайлик:", font=("Arial", 14, "bold"))
    title.pack(pady=10)

    btn_frame = CTkFrame(avatar_window, fg_color="transparent")
    btn_frame.pack(pady=5)

    emojis = ["😎", "😢", "😡"]
    for emo in emojis:
        btn = CTkButton(btn_frame, text=emo, font=("Arial", 22), width=60, height=50,
                        command=lambda e=emo: change_avatar(e))
        btn.pack(side="left", padx=10)


# === ЛЕВАЯ ПАНЕЛЬ: ПРОФИЛЬ USER ===
profile_frame = CTkFrame(window, corner_radius=10)
profile_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Зона аватарки
avatar = CTkLabel(profile_frame, text="😎", font=("Arial", 50), width=100, height=100, fg_color="#3b3b3b",
                  corner_radius=50)
avatar.pack(pady=(20, 2))

edit_avatar_btn = CTkButton(profile_frame, text="✏️ Змінити аватарку", width=120, height=24, font=("Arial", 11),
                            fg_color="#1f6aa5")
edit_avatar_btn.configure(command=open_avatar_selector)
edit_avatar_btn.pack(pady=(0, 10))

username_label = CTkLabel(profile_frame, text=nickname, font=("Arial", 16, "bold"))
username_label.pack(pady=5)

# Опис профілю
bio_title = CTkLabel(profile_frame, text="Опис профілю:", font=("Arial", 12, "bold"))
bio_title.pack(anchor="w", padx=20, pady=(10, 0))

bio_text = CTkTextbox(profile_frame, width=240, height=60)
bio_text.insert("0.0", "Люблю програмувати на Python та грати в ігри.")
bio_text.pack(padx=20, pady=5)

# Вибір Країни
country_title = CTkLabel(profile_frame, text="Країна:", font=("Arial", 12, "bold"))
country_title.pack(anchor="w", padx=20, pady=(5, 0))

country_combo = CTkComboBox(profile_frame, width=240,
                            values=["Україна", "Польща", "США", "Німеччина", "Велика Британія"])
country_combo.set("Україна")
country_combo.pack(padx=20, pady=5)

# Вибір Статі
gender_title = CTkLabel(profile_frame, text="Стать:", font=("Arial", 12, "bold"))
gender_title.pack(anchor="w", padx=20, pady=(5, 0))

gender_combo = CTkComboBox(profile_frame, width=240, values=["Чоловіча", "Жіноча"])
gender_combo.set("Чоловіча")
gender_combo.pack(padx=20, pady=5)

# Поле введення віку
age_title = CTkLabel(profile_frame, text="Вік:", font=("Arial", 12, "bold"))
age_title.pack(anchor="w", padx=20, pady=(5, 0))

age_entry = CTkEntry(profile_frame, width=240, placeholder_text="Введіть свій вік...")
age_entry.pack(padx=20, pady=5)
age_entry.bind("<FocusOut>", check_age)
age_entry.bind("<Return>", check_age)

# Улюблена гра
game_title = CTkLabel(profile_frame, text="Улюблена гра:", font=("Arial", 12, "bold"), text_color="#ff6b6b")
game_title.pack(anchor="w", padx=20, pady=(15, 0))

game_entry = CTkEntry(profile_frame, width=240, placeholder_text="Введіть гру та натисніть Enter...")
game_entry.pack(padx=20, pady=5)

game_entry.bind("<FocusOut>", check_game)
game_entry.bind("<Return>", check_game)

theme_switch = CTkSwitch(profile_frame, text="Світла тема", command=toggle_theme)
theme_switch.pack(pady=(20, 5))

# === ПРАВАЯ ПАНЕЛЬ: ЧАТ ===
chat_frame = CTkFrame(window, fg_color="transparent")
chat_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

g = CTkTextbox(chat_frame, width=600, height=400)
g.configure(state="disabled")
g.pack(fill="both", expand=True, pady=(0, 10))

g.bind("<Double-Button-1>", clear_chat_history)

h = CTkEntry(chat_frame, width=600, height=50, placeholder_text="Введіть повідомлення...")
h.pack(fill="x", pady=5)

a = CTkButton(chat_frame, text="надіслати", command=send_msg)
a.pack(anchor="e", pady=5)


# --- СТАРТ ПРИЛОЖЕНИЯ ---
def start_app():
    ask_nickname()
    connect_to_server()


window.after(200, start_app)
window.mainloop()
