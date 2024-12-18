import socket
import threading
import json


class Server:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.messages = {}  # Для хранения сообщений пользователей (offline)
        self.is_running = True

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server running on {self.host}:{self.port}")

        try:
            while self.is_running:
                client_socket, address = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            server_socket.close()
            print("Server stopped.")

    def handle_client(self, client_socket, address):
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                return

            try:
                request = json.loads(data)
            except json.JSONDecodeError:
                client_socket.send(json.dumps({"status": "error", "message": "Invalid JSON format."}).encode())
                return

            action = request.get("action")

            if action == "send_message":
                sender = request.get("sender")
                recipient = request.get("recipient")
                message = request.get("message")

                if not sender or not recipient or not message:
                    client_socket.send(json.dumps({"status": "error", "message": "Invalid data."}).encode())
                    return

                # Сохранить сообщение для получателя
                if recipient not in self.messages:
                    self.messages[recipient] = []
                self.messages[recipient].append({"from": sender, "message": message})

                client_socket.send(json.dumps({"status": "success", "message": "Message sent."}).encode())
                print(f"Message from {sender} to {recipient}: {message}")

            elif action == "get_messages":
                recipient = request.get("recipient")
                if not recipient:
                    client_socket.send(json.dumps({"status": "error", "message": "Invalid data."}).encode())
                    return

                # Вернуть сообщения для получателя
                user_messages = self.messages.pop(recipient, [])
                client_socket.send(json.dumps({"status": "success", "messages": user_messages}).encode())
                print(f"Messages delivered to {recipient}: {user_messages}")

        except Exception as e:
            print(f"Error while handling client {address}: {e}")
        finally:
            client_socket.close()

import socket
import json


class Client:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port

    def send_request(self, request):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                client_socket.send(json.dumps(request).encode())
                response = client_socket.recv(1024).decode()
                return json.loads(response)
        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error", "message": str(e)}

    def send_message(self, sender, recipient, message):
        request = {
            "action": "send_message",
            "sender": sender,
            "recipient": recipient,
            "message": message,
        }
        response = self.send_request(request)
        print(f"Response: {response}")

    def get_messages(self, recipient):
        request = {"action": "get_messages", "recipient": recipient}
        response = self.send_request(request)
        if response["status"] == "success":
            print(f"Messages for {recipient}: {response.get('messages', [])}")
        else:
            print(f"Error: {response.get('message')}")


# Example usage
if __name__ == "__main__":
    client = Client()

    # Отправить сообщение
    client.send_message(sender="User1", recipient="User2", message="Hello, User2!")

    # Получить сообщения
    client.get_messages(recipient="User2")