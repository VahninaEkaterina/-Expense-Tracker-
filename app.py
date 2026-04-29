import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
import uuid

DATA_FILE = "expenses.json"
CATEGORIES = ["Еда", "Транспорт", "Развлечения", "Быт", "Здоровье", "Другое"]

def load_data():
    """Загружает данные из JSON-файла с обработкой ошибок."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка данных", "Файл данных повреждён. Будет создан новый файл.")
        return []
    except IOError as e:
        messagebox.showerror("Ошибка ввода-вывода", f"Не удалось прочитать файл: {e}")
        return []

def save_data(data):
    """Сохраняет данные в JSON-файл с обработкой ошибок."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        messagebox.showerror("Ошибка записи", f"Не удалось сохранить данные: {e}")

def validate_amount(amount_str):
    """Проверяет, что сумма — положительное число."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля.")
        return amount
    except ValueError:
        raise ValueError("Введите корректную сумму (положительное число).")

def validate_date(date_str):
    """Проверяет, что дата в формате ГГГГ-ММ-ДД."""
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД (например, 2026-04-29).")

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = load_data()

        # --- Блок ввода данных ---
        input_frame = ttk.LabelFrame(root, text="Добавить расход")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.category_var = tk.StringVar(value=CATEGORIES[0])
        self.category_menu = ttk.Combobox(input_frame, textvariable=self.category_var, values=CATEGORIES)
        self.category_menu.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.insert(0, datetime.date.today().isoformat())
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_btn = ttk.Button(input_frame, text="Добавить расход", command=self.add_expense)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Блок фильтрации ---
        filter_frame = ttk.LabelFrame(root, text="Фильтр")
        filter_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="we")

        ttk.Label(filter_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=2)
        self.filter_category = ttk.Combobox(filter_frame, values=["Все"] + CATEGORIES)
        self.filter_category.current(0)
        self.filter_category.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Дата с:").grid(row=1, column=0, padx=5, pady=2)
        self.filter_date_from = ttk.Entry(filter_frame)
        self.filter_date_from.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Дата по:").grid(row=2, column=0, padx=5, pady=2)
        self.filter_date_to = ttk.Entry(filter_frame)
        self.filter_date_to.grid(row=2, column=1, padx=5, pady=2)

        self.apply_filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.apply_filter_btn.grid(row=3, column=0, columnspan=2, pady=(5, 2))

         # --- Таблица расходов ---
         cols = ("id", "Дата", "Категория", "Сумма")
         self.tree = ttk.Treeview(root, columns=cols, show="headings")
         
         # Настройка ширины колонок
         self.tree.column("id", width=30)
         self.tree.column("Дата", width=120)
         self.tree.column("Категория", width=120)
         self.tree.column("Сумма", width=100)
         
         for col in cols:
             self.tree.heading(col, text=["ID", "Дата", "Категория", "Сумма"][cols.index(col)])
         
         self.tree.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="we")

         # --- Подсчёт суммы ---
         self.sum_label = ttk.Label(root, text="Сумма расходов: 0.00 ₽")
         self.sum_label.grid(row=3, column=0, sticky="w", padx=10)

         # Загрузка данных при старте
         self.display_data()

    def add_expense(self):
         try:
             amount = validate_amount(self.amount_entry.get())
             category = self.category_var.get()
             date = validate_date(self.date_entry.get())

             expense = {
                 "id": str(uuid.uuid4()), # Генерация уникального ID
                 "date": date.isoformat(),
                 "category": category,
                 "amount": amount
             }
             self.data.append(expense)
             save_data(self.data)
             self.display_data()
             messagebox.showinfo("Успех", "Расход добавлен!")
             
             # Очистка полей после добавления
             self.amount_entry.delete(0, tk.END)
             self.date_entry.delete(0, tk.END)
             self.date_entry.insert(0, datetime.date.today().isoformat())
             
         except ValueError as e:
             messagebox.showerror("Ошибка ввода", str(e))

    def display_data(self):
         for i in self.tree.get_children():
             self.tree.delete(i)

         filtered = self.data.copy()
         
         # Фильтрация по категории
         cat = self.filter_category.get()
         if cat != "Все":
             filtered = [e for e in filtered if e["category"] == cat]

         # Фильтрация по дате (если указаны обе даты)
         date_from_str = self.filter_date_from.get()
         date_to_str = self.filter_date_to.get()
         
         if date_from_str and date_to_str:
             try:
                 df = validate_date(date_from_str)
                 dt = validate_date(date_to_str)
                 filtered = [e for e in filtered if df <= datetime.date.fromisoformat(e["date"]) <= dt]
             except ValueError as e:
                 messagebox.showerror("Ошибка даты", str(e))
                 return

         for e in filtered:
             self.tree.insert("", "end", values=(e["id"], e["date"], e["category"], f"{e['amount']:.2f} ₽"))

         total = sum(e['amount'] for e in filtered)
         self.sum_label.config(text=f"Сумма расходов: {total:.2f} ₽")

    def apply_filter(self):
         self.display_data()

if __name__ == "__main__":
     root = tk.Tk()
     app = ExpenseTrackerApp(root)
     root.mainloop()
