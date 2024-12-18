import sys
import threading
import socket
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QTextEdit, QMessageBox
)
from PySide6.QtCore import QTimer


# Server Code
class Server:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.clients = {}
        self.messages = {}
        self.is_running = True  # Флаг работы сервера

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        server_socket.settimeout(1.0)  # Тайм-аут для выхода из блокировки accept
        print(f"Server running on {self.host}:{self.port}")

        try:
            while self.is_running:
                try:
                    client_socket, address = server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            server_socket.close()
            print("Server stopped.")

    def handle_client(self, client_socket, address):
        try:
            username = None

            while True:
                try:
                    data = client_socket.recv(1024).decode()
                    if not data:  # Если соединение закрыто клиентом
                        break

                    try:
                        request = json.loads(data)
                    except json.JSONDecodeError:
                        client_socket.send(json.dumps({"status": "error", "message": "Invalid JSON format."}).encode())
                        continue

                    action = request.get("action")

                    if action == "register":
                        username = request.get("username")
                        if username in self.clients:
                            client_socket.send(json.dumps({"status": "error", "message": "Username already taken."}).encode())
                        else:
                            self.clients[username] = (client_socket, address)
                            self.messages[username] = {}
                            client_socket.send(json.dumps({"status": "success", "message": "Registered successfully."}).encode())
                            print(f"User registered: {username}")

                    elif action == "login":
                        username = request.get("username")
                        if username in self.clients:
                            client_socket.send(json.dumps({"status": "error", "message": "User already logged in."}).encode())
                        else:
                            self.clients[username] = (client_socket, address)
                            client_socket.send(json.dumps({"status": "success", "message": "Logged in successfully."}).encode())
                            print(f"User logged in: {username}")

                    elif action == "logout":
                        if username in self.clients:
                            del self.clients[username]
                            print(f"User logged out: {username}")
                        break

                    elif action == "get_online_users":
                        online_users = list(self.clients.keys())
                        client_socket.send(json.dumps({"status": "success", "users": online_users}).encode())

                    elif action == "send_message":
                        recipient = request.get("recipient")
                        message = request.get("message")
                        if recipient in self.clients:
                            if recipient not in self.messages[username]:
                                self.messages[username][recipient] = []
                            self.messages[username][recipient].append(message)
                            self.clients[recipient][0].send(json.dumps({"action": "receive_message", "from": username, "message": message}).encode())
                            print(f"Message from {username} to {recipient}: {message}")
                        else:
                            client_socket.send(json.dumps({"status": "error", "message": "Recipient not online."}).encode())

                except Exception as e:
                    print(f"Error while handling client {address}: {e}")
                    break
        finally:
            if username and username in self.clients:
                del self.clients[username]
                print(f"User disconnected: {username}")
            client_socket.close()


# Client Code
class ClientApp(QMainWindow):
    def __init__(self, host="127.0.0.1", port=12345):
        super().__init__()

        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

        self.init_ui()
        self.connect_to_server()

    def init_ui(self):
        self.setWindowTitle("Chat Client")

        layout = QVBoxLayout()

        self.login_widget = QWidget()
        login_layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        login_layout.addWidget(self.username_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        login_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        login_layout.addWidget(self.register_button)

        self.login_widget.setLayout(login_layout)
        layout.addWidget(self.login_widget)

        self.chat_widget = QWidget()
        chat_layout = QVBoxLayout()

        self.online_users = QListWidget()
        chat_layout.addWidget(QLabel("Online Users"))
        chat_layout.addWidget(self.online_users)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        chat_layout.addWidget(QLabel("Chat History"))
        chat_layout.addWidget(self.chat_history)

        self.message_input = QLineEdit()
        chat_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send Message")
        self.send_button.clicked.connect(self.send_message)
        chat_layout.addWidget(self.send_button)

        self.chat_widget.setLayout(chat_layout)
        layout.addWidget(self.chat_widget)

        self.chat_widget.hide()

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_online_users)

    def connect_to_server(self):
        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            self.chat_history.append(f"Error connecting to server: {e}")

    def login(self):
        username = self.username_input.text()
        if not username:
            return

        self.send_request({"action": "login", "username": username})
        response = self.receive_response()

        if response.get("status") == "success":
            self.username = username
            self.login_widget.hide()
            self.chat_widget.show()
            self.timer.start(2000)  # Update online users every 2 seconds

    def register(self):
        username = self.username_input.text()
        if not username:
            return

        self.send_request({"action": "register", "username": username})
        response = self.receive_response()

        if response.get("status") == "success":
            self.login()

    def send_message(self):
        selected_user = self.online_users.currentItem()
        if not selected_user:
            return

        recipient = selected_user.text()
        message = self.message_input.text()
        if not message:
            return

        self.send_request({"action": "send_message", "recipient": recipient, "message": message})
        self.chat_history.append(f"To {recipient}: {message}")
        self.message_input.clear()

    def update_online_users(self):
        self.send_request({"action": "get_online_users"})
        response = self.receive_response()
        if response.get("status") == "success":
            self.online_users.clear()
            for user in response.get("users", []):
                if user != self.username:
                    self.online_users.addItem(user)

    def send_request(self, request):
        try:
            self.socket.send(json.dumps(request).encode())
        except Exception as e:
            self.chat_history.append(f"Error sending request: {e}")

    def receive_response(self):
        try:
            data = self.socket.recv(1024).decode()
            if not data:  # Если сервер закрыл соединение
                self.chat_history.append("Disconnected from server.")
                self.socket.close()
                return {}
            response = json.loads(data)
            if response.get("action") == "receive_message":
                sender = response.get("from")
                message = response.get("message")
                self.show_message_notification(sender, message)
            return response
        except json.JSONDecodeError:
            self.chat_history.append("Received invalid JSON.")
        except Exception as e:
            self.chat_history.append(f"Error receiving response: {e}")
        return {}

    def show_message_notification(self, sender, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("New Message")
        msg_box.setText(f"Message from {sender}:\n{message}")
        msg_box.exec()

    def closeEvent(self, event):
        if self.username:
            self.send_request({"action": "logout"})
        self.socket.close()
        event.accept()


# Run Server and Client
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        server = Server()
        server.start()
    else:
        app = QApplication(sys.argv)
        client = ClientApp()
        client.show()
        sys.exit(app.exec())
