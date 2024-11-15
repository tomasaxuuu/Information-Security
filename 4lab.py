import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

random_sequence = []
# Создание основного окна
root = tk.Tk()
root.title("Генератор случайных последовательностей и шифрование")
root.geometry("600x400")

# Переменные для интерфейса
password_var = tk.StringVar()
hashed_password_var = tk.StringVar()  # Для отображения хэшированного пароля

# Таблица для MaHash4v64
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
    data = bytearray(password.encode())
    hashed_password = MaHash4v64(data)
    hashed_password_var.set(f"Хешированный пароль: {hashed_password}")
    return hashed_password

def permutation_cipher(data, n, m, reverse=False):
    """Блочное шифрование перестановкой (блок 8 байт)"""
    block_size = 8
    processed_data = bytearray()

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        if len(block) < block_size:
            block = block.ljust(block_size, b'\0')

        if reverse:
            processed_block = inverse_permute_block(block, n, m)
        else:
            processed_block = permute_block(block, n, m)

        processed_data.extend(processed_block)

    return processed_data

def permute_block(block, n, m):
    """Функция перестановки в блоке для шифрования"""
    if n >= m or m > len(block):
        raise ValueError("Неверные границы подблоков")

    # Переставляем подблоки: третий -> первый, второй остается, первый -> третий
    first_part = block[:n]
    second_part = block[n:m]
    third_part = block[m:]
    return third_part + second_part + first_part

def inverse_permute_block(block, n, m):
    """Обратная перестановка для восстановления исходного блока при дешифровании"""
    third_part = block[:len(block) - m]
    second_part = block[len(block) - m:len(block) - n]
    first_part = block[len(block) - n:]
    return first_part + second_part + third_part


def get_permutation_bounds(hashed_password):
    hash_bytes = hashed_password.to_bytes(8, 'big')
    n = hash_bytes[0] % 4 + 1
    m = hash_bytes[1] % 4 + 5

    return n, m
def encrypt_file(file_data, password):
    hashed_password = hash_password(password)
    n, m = get_permutation_bounds(hashed_password)
    encrypted_data = permutation_cipher(file_data, n, m, reverse=False)
    return hashed_password.to_bytes(8, 'big') + encrypted_data

def decrypt_file(file_data, password):
    expected_hash = int.from_bytes(file_data[:8], 'big')
    actual_hash = hash_password(password)

    if actual_hash != expected_hash:
        messagebox.showerror("Ошибка", "Неверный пароль!")
        return file_data

    n, m = get_permutation_bounds(actual_hash)
    return permutation_cipher(file_data[8:], n, m, reverse=True)


def process_encryption():
    """Шифрование файла"""
    password = password_var.get()
    if not password:
        messagebox.showerror("Ошибка", "Введите пароль для шифрования!")
        return

    filename = open_file()
    if not filename:
        return

    try:
        with open(filename, "rb") as file:
            file_data = file.read()

        encrypted_data = encrypt_file(file_data, password)
        save_data(encrypted_data, "Файл успешно зашифрован!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при шифровании: {str(e)}")

def process_decryption():
    """Дешифрование файла"""
    password = password_var.get()
    if not password:
        messagebox.showerror("Ошибка", "Введите пароль для дешифрования!")
        return

    filename = open_file()
    if not filename:
        return

    try:
        with open(filename, "rb") as file:
            file_data = file.read()

        decrypted_data = decrypt_file(file_data, password)
        save_data(decrypted_data, "Файл успешно дешифрован!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при дешифровании: {str(e)}")

def open_file():
    """Открытие файла"""
    return filedialog.askopenfilename(title="Открыть файл для шифрования/дешифрования")

def save_data(data, success_message):
    """Сохранение данных в файл"""
    save_path = filedialog.asksaveasfilename(title="Сохраните файл как", defaultextension=".txt")
    if save_path:
        with open(save_path, "wb") as file:
            file.write(data)
        messagebox.showinfo("Успех", success_message)

# Элементы интерфейса
tk.Label(root, text="Введите пароль для шифрования/дешифрования:").pack(pady=10)
tk.Entry(root, textvariable=password_var, show="*").pack()
tk.Label(root, textvariable=hashed_password_var).pack(pady=10)

# Кнопки для шифрования и дешифрования
tk.Button(root, text="Зашифровать файл", command=process_encryption).pack(pady=10)
tk.Button(root, text="Дешифровать файл", command=process_decryption).pack(pady=10)

# Запуск интерфейса
root.mainloop()
