import os
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import numpy as np

random_sequence = []

# Создание основного окна
root = tk.Tk()
root.title("Генератор случайных последовательностей")
root.geometry("800x600")

sequence_length_var = tk.StringVar()

progress_var = tk.DoubleVar()
status_text = tk.StringVar()

# Создание стиля для прогресс-бара с зелёной заливкой
style = ttk.Style()
style.configure("Green.Horizontal.TProgressbar", troughcolor='white', background='green')

def update_progress_bar(value):
    """Обновление прогресс-бара (от 0 до 100)"""
    progress_var.set(int(value * 100))
    root.update_idletasks()


def create_random_bits():
    """Создание случайной последовательности битов с обновлением прогресс-бара"""
    global random_sequence
    feedback = ""
    input_val = sequence_length_var.get()

    if not input_val:
        messagebox.showerror("Ошибка", "Длина последовательности не может быть пустой")
        return

    try:
        sequence_length = int(input_val)
        if sequence_length > 0:
            random_sequence = []
            step = max(sequence_length // 100, 1)  # Шаг для обновления прогресса

            for i in range(sequence_length):
                random_sequence.append(random.randint(0, 1))
                if i % step == 0 or i == sequence_length - 1:
                    progress = (i + 1) / sequence_length
                    update_progress_bar(progress)

            filename = "sequence.txt"
            with open(filename, "w") as file:
                file.write(str(random_sequence))
            feedback = "Последовательность успешно создана и сохранена в файл."
            status_text.set(feedback)
            print(feedback)  # Вывод в консоль
            update_progress_bar(1.0)  # Устанавливаем прогресс на 100% в конце
        else:
            messagebox.showerror("Ошибка", "Длина последовательности должна быть больше 0")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный ввод длины")


def bit_pattern_test():
    """Первый тест на случайность"""
    if not all(bit in (0, 1) for bit in random_sequence):
        raise ValueError("Последовательность должна содержать только 0 и 1.")

    n = len(random_sequence)
    X = [2 * bit - 1 for bit in random_sequence]
    Sn = sum(X)
    S = abs(Sn) / (n ** 0.5)
    result = f"S: {S} \n"

    if S <= 1.82138636:
        result += "Последовательность прошла тест на случайность."
    else:
        result += "Последовательность не прошла тест на случайность."

    status_text.set(result)
    print("Первый тест на случайность:")
    print(result)  # Вывод в консоль


def identical_bits_test():
    """Второй тест на идентичные биты"""
    if not all(bit in (0, 1) for bit in random_sequence):
        raise ValueError("Последовательность должна содержать только 0 и 1.")

    n = len(random_sequence)
    pi = sum(random_sequence) / n
    Vn = 1 + sum(1 for k in range(n - 1) if random_sequence[k] != random_sequence[k + 1])
    S = abs(Vn - 2 * n * pi * (1 - pi)) / (2 * (2 ** 0.5) * n * pi * (1 - pi) ** 0.5)
    result = f"S: {S} \n"

    if S <= 1.82138636:
        result += "Последовательность прошла тест на случайность."
    else:
        result += "Последовательность не прошла тест на случайность."

    status_text.set(result)
    print("Тест на идентичные биты:")
    print(result)  # Вывод в консоль


def deviation_test():
    """Тест на отклонения с выводом состояний от -9 до 9"""
    x_values = 2 * np.array(random_sequence) - 1
    cumulative_sum = np.cumsum(x_values)
    cumulative_sum = np.concatenate(([0], cumulative_sum, [0]))
    zero_count = np.sum(cumulative_sum == 0) - 1

    # Определяем диапазон значений для `counts`, включая -9 и 9
    counts = np.zeros(19)  # диапазон от -9 до 9, то есть 19 значений

    # Заполняем массив `counts`, фильтруя только значения от -9 до 9
    for state in cumulative_sum:
        if -9 <= state <= 9:
            counts[int(state) + 9] += 1  # `+9` для смещения индексов от 0 до 18

    y_values = np.zeros(19)  # аналогично, только для диапазона от -9 до 9
    for j in range(19):
        abs_j = abs(j - 9)  # корректное преобразование индекса в состояние
        if 2 * zero_count * (4 * abs_j - 2) > 0:
            y_values[j] = abs(counts[j] - zero_count) / np.sqrt(2 * zero_count * (4 * abs_j - 2))

    result = "Результаты теста на отклонения (состояния от -9 до 9):\n"
    for j in range(-9, 10):
        index = j + 9
        result += f"Состояние {j}: {int(counts[index])} раз, Статистика: {y_values[index]:.4f} \n"

    if np.all(y_values <= 1.82138636):
        result += "Последовательность прошла тест на случайность."
    else:
        result += "Последовательность не прошла тест на случайность."

    status_text.set(result)
    print("Тест на отклонения:")
    print(result)  # Вывод в консоль


# Элементы интерфейса
tk.Label(root, text="Длина последовательности:").pack()
tk.Entry(root, textvariable=sequence_length_var).pack()

tk.Button(root, text="Создать последовательность", command=create_random_bits).pack(pady=10)
tk.Button(root, text="Тест на случайность", command=bit_pattern_test).pack(pady=5)
tk.Button(root, text="Тест на идентичные биты", command=identical_bits_test).pack(pady=5)
tk.Button(root, text="Тест на отклонения", command=deviation_test).pack(pady=5)

tk.Label(root, textvariable=status_text, wraplength=750).pack(pady=20)

# Создание статичного прогресс-бара с зелёной заливкой
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, style="Green.Horizontal.TProgressbar")
progress_bar.pack(fill="x", padx=20, pady=20)

# Запуск интерфейса
root.mainloop()
