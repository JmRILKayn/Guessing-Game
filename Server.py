import random
import socket

class GuessingGameServer:
    def __init__(self, host="192.168.254.105", port=7777, password="jmpogi123"):
        self.host = host
        self.port = port
        self.password = password
        self.secret_number = random.randint(1, 100)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")
            with conn:
                conn.sendall("Enter password:\n".encode())
                client_password = conn.recv(1024).decode().strip()

                if client_password != self.password:
                    conn.sendall("Incorrect password. Connection closed.".encode())
                    conn.close()
                    print(f"Connection closed for {addr} due to invalid password.")
                    continue

                conn.sendall("Password accepted! Start guessing the number (1-100):\n".encode())

                guess_count = 0
                while True:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break
                    try:
                        guess = int(data)
                        guess_count += 1
                        if guess < self.secret_number:
                            response = "Too low!"
                        elif guess > self.secret_number:
                            response = "Too high!"
                        else:
                            if guess_count <= 5:
                                rating = "Excellent"
                            elif guess_count <= 20:
                                rating = "Very Good"
                            else:
                                rating = "Good/fair"
                            response = f"Correct! You win! Rating: {rating}"
                            self.secret_number = random.randint(1, 100)
                            guess_count = 0
                        conn.sendall(response.encode())
                    except ValueError:
                        conn.sendall("Invalid input! Please enter a number.".encode())

    def stop(self):
        self.server_socket.close()

def main():
    server = GuessingGameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.stop()

if __name__ == "__main__":
    main()