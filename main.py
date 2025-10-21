# main.py
import tkinter as tk
from tkinter import messagebox
from models import Order

# Основное окно приложения
root = tk.Tk()
root.title("Приложение заказов")
root.geometry("400x400")

# Поля ввода
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

def refresh_list():
    """Обновление списка заказов"""
    orders_listbox.delete(0, tk.END)
    for order in Order.select():
        orders_listbox.insert(tk.END, f"{order.id}. {order.name} — {order.quantity}")

def add_order():
    """Добавление нового заказа"""
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
    """Удаление выбранного заказа"""
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
    """Изменение выбранного заказа"""
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

# Кнопки управления
add_button = tk.Button(root, text="Добавить", command=add_order)
add_button.pack()

update_button = tk.Button(root, text="Изменить", command=update_order)
update_button.pack()

delete_button = tk.Button(root, text="Удалить", command=delete_order)
delete_button.pack()

refresh_button = tk.Button(root, text="Обновить список", command=refresh_list)
refresh_button.pack(pady=5)

# Начальная загрузка списка
refresh_list()

root.mainloop()
