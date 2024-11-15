import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

random_sequence = []

# Создание основного окна
root = tk.Tk()
root.title("Генератор случайных последовательностей и шифрование")
root.geometry("1200x800")

# Переменные для интерфейса
a_var = 1664525
b_var = 1013904223
m_var = 2**32
x0_var = 42  # Начальное значение X0
progress_var = tk.DoubleVar()
status_text = tk.StringVar()
password_var = tk.StringVar()
hashed_password_var = tk.StringVar()  # Переменная для хэшированного пароля
mask_sequence = []  # Переменная для маски

# Создание стиля для прогресс-бара с зелёной заливкой
style = ttk.Style()
style.configure("Green.Horizontal.TProgressbar", troughcolor='white', background='green')

# Таблица sTable
sTable = [
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F,
    0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F,
    0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F,
    0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F,
    0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F,
    0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F,
    0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0x9B, 0x9C, 0x9D, 0x9E, 0x9F,
    0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF,
    0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,
    0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD, 0xCE, 0xCF,
    0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF,
    0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF,
    0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF
]

def LROT(x):
    """Циклический сдвиг влево на 11 бит"""
    return ((x << 11) & 0xFFFFFFFF) | (x >> 21)

def RROT(x):
    """Циклический сдвиг вправо на 11 бит"""
    return ((x >> 11) & 0xFFFFFFFF) | (x << 21)

def MaHash4v64(data):
    """Реализация MaHash4v64 на Python"""
    len_data = len(data)
    hash1 = len_data
    hash2 = len_data

    for i in range(len_data):
        val = data[i]
        hash1 += sTable[(val + i) & 255]
        hash1 = LROT(hash1 + ((hash1 << 6) ^ (hash1 >> 8)))

        hash2 += sTable[(val + i) & 255]
        hash2 = RROT(hash2 + ((hash2 << 6) ^ (hash2 >> 8)))

        sh1 = hash1
        sh2 = hash2
        hash1 = ((sh1 >> 16) & 0xFFFF) | ((sh2 & 0xFFFF) << 16)
        hash2 = ((sh2 >> 16) & 0xFFFF) | ((sh1 & 0xFFFF) << 16)

    # Собираем результат
    digest = ((hash2 & 0xFFFFFFFF) << 32) | (hash1 & 0xFFFFFFFF)

    return digest

def hash_password(password):
    """Хеширование пароля с использованием MaHash4v64"""
    data = bytearray(password.encode())  # Преобразуем строку пароля в байты
    hashed_password = MaHash4v64(data)  # Хешируем пароль
    hashed_password_var.set(f"Хешированный пароль: {hashed_password}")  # Устанавливаем хеш в текстовое поле
    return hashed_password  # Возвращаем 64-битный хеш как целое число

def initialize_random_with_password(password):
    """Инициализация генератора случайных чисел с использованием хешированного пароля"""
    hashed_seed = hash_password(password)
    random.seed(hashed_seed)

def xor_cipher(data, key):
    """Шифрование и дешифрование с помощью XOR-шифрования"""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def save_file():
    """Выбор пути для сохранения файла"""
    filename = filedialog.asksaveasfilename(title="Сохраните файл как", defaultextension=".txt")
    return filename

def open_file():
    """Открытие файла для шифрования/дешифрования"""
    filename = filedialog.askopenfilename(title="Открыть файл для шифрования/дешифрования")
    return filename

def create_mask_from_sequence():
    """Создание маски для шифрования на основе сгенерированной последовательности"""
    global mask_sequence
    sequence_length = len(mask_sequence)
    mask = [sTable[(val + i) & 255] for i, val in enumerate(mask_sequence)]
    return mask

def encrypt_file(file_data, password, mask):
    """Шифрование файла с использованием пароля и маски"""
    key = hash_password(password).to_bytes(8, 'big')  # Хешируем пароль и используем как ключ (байты)
    masked_data = xor_cipher(file_data, mask)  # Применяем маску
    return xor_cipher(masked_data, key)  # Шифруем данные с использованием пароля

def decrypt_file(file_data, password, mask):
    """Дешифрование файла с использованием пароля и маски"""
    key = hash_password(password).to_bytes(8, 'big')
    unmasked_data = xor_cipher(file_data, key)
    return xor_cipher(unmasked_data, mask)

def create_sequence_and_encrypt():
    """Шифрование файла с использованием сгенерированной маски и пароля"""
    password = password_var.get()
    if not password:
        messagebox.showerror("Ошибка", "Введите пароль для шифрования!")
        return

    # Открываем файл для шифрования
    filename = open_file()
    if not filename:
        return

    try:
        # Считываем данные файла
        with open(filename, "rb") as file:
            file_data = file.read()

        # Получаем размер файла и создаем маску
        file_size = len(file_data)
        create_congruential_sequence(file_size)  # Передаем размер файла в функцию

        # Создаем маску
        mask = create_mask_from_sequence()

        # Шифруем данные
        encrypted_data = encrypt_file(file_data, password, mask)

        # Сохраняем зашифрованный файл
        save_path = save_file()
        if save_path:
            with open(save_path, "wb") as file:
                file.write(encrypted_data)
            messagebox.showinfo("Успех", "Файл успешно зашифрован!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при шифровании: {str(e)}")

def decrypt_selected_file():
    """Дешифрование файла с использованием маски и пароля"""
    password = password_var.get()
    if not password:
        messagebox.showerror("Ошибка", "Введите пароль для дешифрования!")
        return

    # Открываем файл для дешифрования
    filename = open_file()
    if not filename:
        return

    try:
        # Считываем зашифрованные данные файла
        with open(filename, "rb") as file:
            file_data = file.read()

        # Получаем размер файла и создаем маску
        file_size = len(file_data)
        create_congruential_sequence(file_size)

        # Создаем маску
        mask = create_mask_from_sequence()

        # Дешифруем данные
        decrypted_data = decrypt_file(file_data, password, mask)

        # Сохраняем дешифрованный файл
        save_path = save_file()
        if save_path:
            with open(save_path, "wb") as file:
                file.write(decrypted_data)
            messagebox.showinfo("Успех", "Файл успешно дешифрован!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при дешифровании: {str(e)}")

def create_congruential_sequence(file_size):
    """Создание последовательности с использованием линейного конгруэнтного генератора"""
    global mask_sequence
    sequence_length = file_size  # Длина последовательности зависит от размера файла

    try:
        a = a_var
        b = b_var
        m = m_var
        x0 = x0_var

        # Инициализируем генератор псевдослучайных чисел
        mask_sequence = []
        Xn = x0
        for i in range(sequence_length):
            Xn = (a * Xn + b) % m
            mask_sequence.append(Xn % 256)  # Преобразование в байты (0-255)

        messagebox.showinfo("Успех", "Последовательность успешно создана!")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный ввод параметров или длины")

# Элементы интерфейса
tk.Label(root, text="Введите пароль для шифрования/дешифрования:").pack(pady=10)
tk.Entry(root, textvariable=password_var, show="*").pack()

# Отображение хэшированного пароля
tk.Label(root, textvariable=hashed_password_var).pack(pady=10)

# Кнопки для шифрования и дешифрования
tk.Button(root, text="Зашифровать файл", command=create_sequence_and_encrypt).pack(pady=10)
tk.Button(root, text="Дешифровать файл", command=decrypt_selected_file).pack(pady=10)

# Запуск интерфейса
root.mainloop()
