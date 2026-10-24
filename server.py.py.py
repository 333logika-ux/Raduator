from socket import *
from threading import Thread

clients = []

def send_message_for_all(message, client_socket):
    """Рассылает сообщение всем подключенным клиентам, кроме автора"""
    for client in list(clients):
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                if client in clients:
                    clients.remove(client)

def accept_message(client_socket):
    """Принимает сообщения от конкретного клиента в бесконечном цикле"""
    while True:
        try:
            # Буфер увеличен до 4096 для поддержки длинных строк ответов
            message = client_socket.recv(4096).decode()
            if not message:
                break
            print(f"Отримати повідомлення: {message}")
            send_message_for_all(message, client_socket)
        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

# Запуск сервера
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", 7070))
server_socket.listen()

print("SERVER IS RUNNING...")

while True:
    clients_socket, addr = server_socket.accept()
    print(f"Додано клієнта: {addr}")
    clients.append(clients_socket)
    thread = Thread(target=accept_message, args=(clients_socket,), daemon=True)
    thread.start()
