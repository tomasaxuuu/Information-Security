import tkinter as tk
from tkinter import filedialog, messagebox
import random


# Алгоритм Рабина-Миллера
def is_prime_rabin_miller(p, k=40):
    if p < 2:
        return False
    if p in (2, 3):
        return True
    if p % 2 == 0:
        return False

    # Представление p - 1 как 2^b * m
    b = 0
    m = p - 1
    while m % 2 == 0:
        m //= 2
        b += 1

    for _ in range(k):
        a = random.randint(2, p - 2)
        j = 0
        z = pow(a, m, p)

        if z == 1 or z == p - 1:
            continue

        while j < b - 1:
            z = pow(z, 2, p)
            j += 1
            if z == p - 1:
                break
        else:
            return False

    return True


def generate_prime(start):
    while True:
        if is_prime_rabin_miller(start):
            return start
        start += 1


def generate_keys():
    start = 2 ** 127
    p = generate_prime(start)
    g = random.randint(2, p - 2)
    x = random.randint(1, p - 2)  # Закрытый ключ
    y = pow(g, x, p)  # Открытый ключ
    return (p, g, y), x  # (открытый ключ, закрытый ключ)

def encrypt(message, public_key):
    p, g, y = public_key
    k = random.randint(1, p - 2)
    a = pow(g, k, p)
    b = (pow(y, k, p) * message) % p
    return a, b


def decrypt(encrypted_message, private_key, public_key):
    a, b = encrypted_message
    p, _, _ = public_key
    s = pow(a, private_key, p)
    message = (b * pow(s, p - 2, p)) % p
    return message


# --- GUI приложение ---
class ElGamalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Эль-Гамаль Шифрование")

        # Переменные
        self.public_key = None
        self.private_key = None
        self.encrypted_data = None
        self.decrypted_data = None

        # Элементы интерфейса
        self.label1 = tk.Label(root, text="Введите стартовое число для генерации простого числа:")
        self.label1.pack()

        self.entry_start = tk.Entry(root)
        self.entry_start.pack()

        self.button_generate_prime = tk.Button(root, text="Сгенерировать простое число",
                                               command=self.generate_prime_number)
        self.button_generate_prime.pack()

        self.label_prime = tk.Label(root, text="Простое число:")
        self.label_prime.pack()

        self.button_generate_keys = tk.Button(root, text="Сгенерировать ключи", command=self.generate_keys)
        self.button_generate_keys.pack()

        self.label_keys = tk.Label(root, text="Открытый и закрытый ключи:")
        self.label_keys.pack()

        self.button_encrypt = tk.Button(root, text="Зашифровать файл", command=self.encrypt_file)
        self.button_encrypt.pack()

        self.button_decrypt = tk.Button(root, text="Дешифровать файл", command=self.decrypt_file)
        self.button_decrypt.pack()

    def generate_prime_number(self):
        try:
            start = int(self.entry_start.get())
            prime = generate_prime(start)
            self.label_prime.config(text=f"Простое число: {prime}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное стартовое число.")

    def generate_keys(self):
        self.public_key, self.private_key = generate_keys()
        self.label_keys.config(text=f"Открытый ключ: {self.public_key}\nЗакрытый ключ: {self.private_key}")

    def encrypt_file(self):
        if not self.public_key:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключи!")
            return
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:
                data = file.read()
            encrypted_data = [encrypt(byte, self.public_key) for byte in data]
            save_path = filedialog.asksaveasfilename(defaultextension=".txt")
            with open(save_path, "wb") as file:
                for a, b in encrypted_data:
                    # Запись длины a и b и их значений
                    a_bytes = a.to_bytes((a.bit_length() + 7) // 8, 'big')
                    b_bytes = b.to_bytes((b.bit_length() + 7) // 8, 'big')
                    file.write(len(a_bytes).to_bytes(4, 'big') + a_bytes)
                    file.write(len(b_bytes).to_bytes(4, 'big') + b_bytes)
            messagebox.showinfo("Успех", "Файл успешно зашифрован")

    def decrypt_file(self):
        if not self.private_key or not self.public_key:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключи!")
            return
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:
                encrypted_data = []
                while True:
                    len_a_bytes = file.read(4)
                    if not len_a_bytes:
                        break
                    len_a = int.from_bytes(len_a_bytes, 'big')
                    a = int.from_bytes(file.read(len_a), 'big')

                    len_b_bytes = file.read(4)
                    len_b = int.from_bytes(len_b_bytes, 'big')
                    b = int.from_bytes(file.read(len_b), 'big')
                    encrypted_data.append((a, b))
            decrypted_data = bytes([decrypt(pair, self.private_key, self.public_key) for pair in encrypted_data])
            save_path = filedialog.asksaveasfilename(defaultextension=".txt")
            with open(save_path, "wb") as file:
                file.write(decrypted_data)
            messagebox.showinfo("Успех", "Файл успешно расшифрован")


root = tk.Tk()
app = ElGamalApp(root)
root.mainloop()
