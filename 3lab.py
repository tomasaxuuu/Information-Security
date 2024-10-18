import os
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import random


# Генерация случайных чисел с помощью Линейного Конгруэнтного Генератора (LCG)
def lcg(a, b, m, seed, length):
    sequence = []
    Xn = seed
    for _ in range(length):
        Xn = (a * Xn + b) % m
        sequence.append(Xn % 256)  # Преобразуем в байты (0-255)
    return sequence


# Генерация случайных чисел с помощью генератора BBS
def bbs(p, q, seed, length):
    sequence = []
    N = p * q
    x = (seed ** 2) % N
    for _ in range(length):
        x = (x ** 2) % N
        sequence.append(x % 256)  # Преобразуем в байты (0-255)
    return sequence


def hash_password(password):
    """Функция хеширования пароля (временно используем SHA-256 вместо MaHash4v64)"""
    return hashlib.sha256(password.encode()).hexdigest()


def select_file():
    """Выбор файла для шифрования или дешифрования"""
    filename = filedialog.askopenfilename(title="Выберите файл для шифрования/дешифрования")
    return filename


def save_file():
    """Выбор пути для сохранения зашифрованного или расшифрованного файла"""
    filename = filedialog.asksaveasfilename(title="Сохраните файл как", defaultextension=".txt")
    return filename


def xor_cipher(data, key):
    """Шифрование и дешифрование с помощью XOR-шифрования"""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])


def create_key_from_password(password, generator_type):
    """Генерация ключа для шифрования на основе выбранного генератора"""
    hashed_password = hash_password(password)
    seed = int(hashed_password, 16) % 10000  # Используем хеш пароля как seed для генератора

    if generator_type == "LCG":
        # Параметры для линейного конгруэнтного генератора
        a = 1103515245
        b = 12345
        m = 2**31
        key = lcg(a, b, m, seed, 1000)  # Генерация последовательности
    else:
        # Параметры для BBS
        p = 499
        q = 547
        key = bbs(p, q, seed, 1000)  # Генерация последовательности

    return bytearray(key)


def create_key_from_custom(custom_key):
    """Генерация ключа для шифрования на основе пользовательского ключа"""
    return bytearray(custom_key.encode())  # Преобразуем введённый ключ в байты


def encrypt_decrypt_file():
    """Шифрование/Дешифрование файла с использованием пароля и выбранного генератора или пользовательского ключа"""
    if method_var.get() == "generator":
        password = password_entry.get()
        if not password:
            messagebox.showerror("Ошибка", "Введите пароль для генерации ключа!")
            return
    else:
        custom_key = custom_key_entry.get()
        if not custom_key:
            messagebox.showerror("Ошибка", "Введите собственный ключ для шифрования/дешифрования!")
            return

    filename = select_file()
    if not filename:
        return

    try:
        with open(filename, "rb") as f:
            file_data = f.read()

        # Выбор метода шифрования: генератор или пользовательский ключ
        if method_var.get() == "generator":
            generator_type = generator_var.get()
            key = create_key_from_password(password, generator_type)
        else:
            key = create_key_from_custom(custom_key)

        # Шифруем или дешифруем файл с помощью XOR
        encrypted_data = xor_cipher(file_data, key)

        save_path = save_file()
        if save_path:
            with open(save_path, "wb") as f:
                f.write(encrypted_data)
            messagebox.showinfo("Успех", "Файл успешно зашифрован/дешифрован")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")


# Создание графического интерфейса
root = tk.Tk()
root.title("Приложение для шифрования с выбором генератора или собственного ключа")
root.geometry("500x500")

# Поле для ввода пароля
tk.Label(root, text="Введите пароль для шифрования/дешифрования (если используется генератор):").pack(pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=10)

# Радиокнопки для выбора метода (генератор или пользовательский ключ)
method_var = tk.StringVar(value="generator")
tk.Label(root, text="Выберите метод шифрования:").pack(pady=10)
tk.Radiobutton(root, text="Использовать генератор", variable=method_var, value="generator").pack()
tk.Radiobutton(root, text="Использовать собственный ключ", variable=method_var, value="custom").pack()

# Поле для ввода собственного ключа (если выбран пользовательский метод)
custom_key_entry = tk.Entry(root)
tk.Label(root, text="Введите собственный ключ (только для пользовательского метода):").pack(pady=10)
custom_key_entry.pack(pady=10)

# Радиокнопки для выбора генератора (LCG или BBS)
generator_var = tk.StringVar(value="LCG")
tk.Label(root, text="Выберите генератор для шифрования (если выбран генератор):").pack(pady=10)
tk.Radiobutton(root, text="Линейный Конгруэнтный Генератор (LCG)", variable=generator_var, value="LCG").pack()
tk.Radiobutton(root, text="Генератор BBS", variable=generator_var, value="BBS").pack()

# Кнопка для шифрования/дешифрования файла
tk.Button(root, text="Выбрать файл для шифрования/дешифрования", command=encrypt_decrypt_file).pack(pady=20)

# Отображение окна
root.mainloop()
