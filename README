# Приложение для управления заказами на Python с Tkinter и PostgreSQL

Это простое настольное приложение на Python, которое позволяет **создавать, просматривать, изменять и удалять заказы**.
Используется библиотека **Tkinter** для графического интерфейса и **Peewee** для работы с базой данных PostgreSQL.

Проект разделён на **три файла**:

1. `db.py` — подключение к базе данных
2. `models.py` — описание таблицы заказов
3. `main.py` — само приложение с графическим интерфейсом

---

## 🗂 Структура проекта

```
project/
│
├── db.py        # Подключение к базе данных PostgreSQL
├── models.py    # Описание модели "Order"
├── main.py      # Приложение на Tkinter
├── .env         # Файл с конфиденциальными данными для подключения к базе
└── README.md    # Этот файл
```

---

## 📁 Описание файлов

### **1. db.py**

Файл отвечает за подключение к базе данных.

```python
from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

# Загружаем переменные из файла .env
load_dotenv()

# Создаём подключение к PostgreSQL
db = PostgresqlDatabase(
    os.getenv("DB_NAME"),      # Имя базы данных
    user=os.getenv("DB_USER"), # Имя пользователя
    password=os.getenv("DB_PASSWORD"), # Пароль
    host=os.getenv("DB_HOST"), # Адрес сервера базы данных
    port=int(os.getenv("DB_PORT"))     # Порт (обычно 5432)
)
```

**Что делает этот файл:**

* Подключается к вашей базе данных PostgreSQL.
* Использует данные из файла `.env`, чтобы не хранить логины и пароли в коде.

---

### **2. models.py**

Файл описывает **таблицу заказов**.

```python
from peewee import Model, CharField, IntegerField
from db import db

# Модель "Order" — это таблица с заказами
class Order(Model):
    name = CharField()      # Название заказа (текст)
    quantity = IntegerField()  # Количество (число)

    class Meta:
        database = db       # Привязка к базе данных

# Подключаемся к базе и создаём таблицу, если её нет
db.connect()
db.create_tables([Order])
```

**Что делает этот файл:**

* Определяет структуру таблицы с заказами.
* Таблица содержит два поля: название заказа и количество.
* При запуске создаёт таблицу, если она ещё не существует.

---

### **3. main.py**

Главный файл — приложение на Tkinter с графическим интерфейсом.

```python
import tkinter as tk
from tkinter import messagebox
from models import Order

# Создаём главное окно
root = tk.Tk()
root.title("Приложение заказов")
root.geometry("400x400")

# Метки и поля для ввода данных
name_label = tk.Label(root, text="Название заказа:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

quantity_label = tk.Label(root, text="Количество:")
quantity_label.pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

# Список заказов
orders_listbox = tk.Listbox(root, width=50)
orders_listbox.pack(pady=10)

# -------------------
# Функции для работы с заказами
# -------------------

def refresh_list():
    """
    Обновление списка заказов в окне приложения.
    
    - Очищает список заказов в интерфейсе.
    - Загружает все записи из базы данных.
    - Показывает ID, название и количество каждого заказа.
    """
    orders_listbox.delete(0, tk.END)
    for order in Order.select():
        orders_listbox.insert(tk.END, f"{order.id}. {order.name} — {order.quantity}")

def add_order():
    """
    Добавление нового заказа в базу данных.
    
    - Берёт данные из полей ввода.
    - Проверяет, что поля заполнены.
    - Преобразует количество в число.
    - Создаёт новый заказ в базе.
    - Обновляет список заказов на экране.
    - Очищает поля для ввода.
    """
    name = name_entry.get()
    quantity = quantity_entry.get()
    if not name or not quantity:
        messagebox.showwarning("Ошибка", "Заполните все поля")
        return
    try:
        quantity = int(quantity)
        Order.create(name=name, quantity=quantity)
        refresh_list()
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Ошибка", "Количество должно быть числом")

def delete_order():
    """
    Удаление выбранного заказа из базы данных.
    
    - Проверяет, что выбран элемент в списке.
    - Определяет ID заказа по выбранному элементу.
    - Удаляет запись из базы.
    - Обновляет список заказов.
    """
    selected = orders_listbox.curselection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите заказ для удаления")
        return
    item_text = orders_listbox.get(selected[0])
    order_id = int(item_text.split(".")[0])
    order = Order.get_or_none(Order.id == order_id)
    if order:
        order.delete_instance()
        refresh_list()

def update_order():
    """
    Изменение выбранного заказа.
    
    - Проверяет, что выбран элемент в списке.
    - Берёт новые значения из полей ввода.
    - Проверяет, что поля заполнены и количество — число.
    - Сохраняет изменения в базе.
    - Обновляет список заказов.
    """
    selected = orders_listbox.curselection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите заказ для изменения")
        return
    name = name_entry.get()
    quantity = quantity_entry.get()
    if not name or not quantity:
        messagebox.showwarning("Ошибка", "Заполните все поля")
        return
    try:
        quantity = int(quantity)
        item_text = orders_listbox.get(selected[0])
        order_id = int(item_text.split(".")[0])
        order = Order.get_or_none(Order.id == order_id)
        if order:
            order.name = name
            order.quantity = quantity
            order.save()
            refresh_list()
    except ValueError:
        messagebox.showerror("Ошибка", "Количество должно быть числом")

# -------------------
# Кнопки для управления
# -------------------

add_button = tk.Button(root, text="Добавить", command=add_order)
add_button.pack()

update_button = tk.Button(root, text="Изменить", command=update_order)
update_button.pack()

delete_button = tk.Button(root, text="Удалить", command=delete_order)
delete_button.pack()

refresh_button = tk.Button(root, text="Обновить список", command=refresh_list)
refresh_button.pack(pady=5)

# Загружаем список заказов при старте
refresh_list()

# Запуск главного цикла приложения
root.mainloop()
```

---

## ✅ Что делает приложение

* Создаёт окно с полями для ввода: название и количество заказа.
* Отображает все заказы из базы данных в списке с ID, названием и количеством.
* Позволяет:

  * **Добавлять** новые заказы
  * **Изменять** выбранный заказ
  * **Удалять** выбранный заказ
  * **Обновлять** список заказов
* Использует PostgreSQL через Peewee, обеспечивая хранение данных на сервере.


