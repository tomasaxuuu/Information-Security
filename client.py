import socket
import tkinter as tk
from tkinter import messagebox

# Подключение к серверу
def connect_to_server():
    try:
        server_ip = entry_ip.get()
        server_port = int(entry_port.get())
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        return client_socket
    except Exception as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к серверу: {e}")
        return None

# Отправка команды на сервер
def send_command():
    command = entry_command.get()
    client_socket = connect_to_server()
    if client_socket:
        client_socket.send(command.encode())  # Отправляем команду на сервер
        response = client_socket.recv(1024)  # Получаем ответ от сервера
        # Проверяем, является ли ответ строкой или бинарными данными
        try:
            # Если ответ можно декодировать как строку
            decoded_response = response.decode('utf-8')
            messagebox.showinfo("Ответ от сервера", decoded_response)
            if command.lower() == 'bye':  # Если команда 'bye', закрываем окно
                client_socket.close()  # Закрываем соединение
                root.quit()  # Закрытие окна программы
        except UnicodeDecodeError:
            # Если данные не могут быть декодированы как строка, отображаем их как hex
            hex_response = response.hex()  # Конвертируем бинарные данные в строку hex
            # Выводим hex строку в текстовое поле
            text_output.delete(1.0, tk.END)  # Очищаем поле вывода
            text_output.insert(tk.END, hex_response)  # Вставляем зашифрованные данные в текстовое поле
        finally:
            client_socket.close()

# Основное окно
root = tk.Tk()
root.title("Клиент серверного приложения")

# Элементы интерфейса
label_ip = tk.Label(root, text="IP сервера:")
label_ip.grid(row=0, column=0)
entry_ip = tk.Entry(root)
entry_ip.grid(row=0, column=1)

label_port = tk.Label(root, text="Порт сервера:")
label_port.grid(row=1, column=0)
entry_port = tk.Entry(root)
entry_port.grid(row=1, column=1)

label_command = tk.Label(root, text="Команда:")
label_command.grid(row=2, column=0)
entry_command = tk.Entry(root)
entry_command.grid(row=2, column=1)

button_send = tk.Button(root, text="Отправить", command=send_command)
button_send.grid(row=3, column=0, columnspan=2)

# Добавим поле Text для вывода зашифрованных данных
text_output = tk.Text(root, height=10, width=50)
text_output.grid(row=4, column=0, columnspan=2)

root.mainloop()
