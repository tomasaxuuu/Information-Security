import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Функция для шифрования текста или файла
# Функция для шифрования текста или файла
def encrypt_data(data, password):
    # Приводим пароль к длине 16 байт для AES
    key = password.encode('utf-8')[:16].ljust(16, b'\0')  # Дополняем нулями до 16 байт
    iv = os.urandom(16)  # Случайный вектор инициализации
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Дополняем данные до блока 16 байт
    padded_data = data + (b" " * (16 - len(data) % 16))
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted

# Функция для дешифрования данных
def decrypt_data(data, password):
    # Приводим пароль к длине 16 байт для AES
    key = password.encode('utf-8')[:16].ljust(16, b'\0')  # Дополняем нулями до 16 байт
    iv = data[:16]  # Первая часть данных — это вектор инициализации
    encrypted_data = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted.rstrip(b" ")

# Обработка запросов от клиента
def handle_client(client_socket, addr):
    print(f"Подключение от {addr}")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            command, *args = data.split()

            if command.lower() == 'hello':
                response = f"hello variant {args[0]}"
                client_socket.send(response.encode())

            elif command.lower() == 'bye':
                response = f"bye variant {args[0]}"
                client_socket.send(response.encode())
                break

            elif command.lower() == 'encrypt':
                message = ' '.join(args[:-1])
                password = args[-1]
                encrypted_data = encrypt_data(message.encode(), password)
                client_socket.send(encrypted_data)

            elif command.lower() == 'decrypt':
                encrypted_data = bytes.fromhex(' '.join(args[:-1]))
                password = args[-1]
                decrypted_data = decrypt_data(encrypted_data, password)
                client_socket.send(decrypted_data)

            else:
                client_socket.send("Неизвестная команда.".encode())

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

# Запуск сервера
def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
