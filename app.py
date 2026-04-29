import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Еда", "Транспорт", "Развлечения", "Быт", "Здоровье", "Другое"]

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
        return amount
    except ValueError:
        raise ValueError("Сумма должна быть положительным числом.")

def validate_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД (например, 2026-04-29).")

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = load_data()

        # --- Ввод данных ---
        ttk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.Вот готовая структура папки и файлов для проекта «Expense Tracker» (трекер расходов) с использованием Python, Tkinter, JSON и Git. Вы можете создать такую структуру на своём компьютере, добавить в неё указанные файлы и загрузить в GitHub.

### Структура папки проекта
