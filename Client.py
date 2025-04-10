import socket

class GuessingGameClient:
    def __init__(self, host="192.168.254.105", port=7777):
        self.host = host
        self.port = port

    def play(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            
         
            prompt = client_socket.recv(1024).decode()
            print(prompt, end='')
            password = input()
            client_socket.sendall(password.encode())

          
            response = client_socket.recv(1024).decode()
            print(response)
            if "Incorrect" in response:
                return  

           
            while True:
                guess = input("Enter your guess (1-100): ")
                client_socket.sendall(guess.encode())
                response = client_socket.recv(1024).decode()
                print(response)
                if "Correct!" in response:
                    break

def main():
    client = GuessingGameClient()
    try:
        client.play()
    except KeyboardInterrupt:
        print("Stopping client")
    finally:
        pass

if __name__ == "__main__":
    main()
