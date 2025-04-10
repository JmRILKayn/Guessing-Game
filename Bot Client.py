import socket
import time

class GuessingGameBot:
    def __init__(self, host="192.168.254.105", port=7777):
        self.host = host
        self.port = port

    def play(self):
        password = input("Enter server password: ")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bot_socket:
            bot_socket.connect((self.host, self.port))
            
            prompt = bot_socket.recv(1024).decode()
            print(prompt, end='')

    
            bot_socket.sendall(password.encode())


            response = bot_socket.recv(1024).decode()
            print(response)
            if "Incorrect" in response:
                return


            low = 1
            high = 100
            guess_count = 0

            while True:
                guess = (low + high) // 2
                print(f"Bot guesses: {guess}")
                bot_socket.sendall(str(guess).encode())
                guess_count += 1

                response = bot_socket.recv(1024).decode()
                print(f"Server says: {response}")

                if "Too low" in response:
                    low = guess + 1
                elif "Too high" in response:
                    high = guess - 1
                elif "Correct!" in response:
                    print(f"Bot won in {guess_count} guesses!")
                    break
                else:
                    print("Unexpected response from server.")
                    break

                time.sleep(0.4)  

def main():
    bot = GuessingGameBot()
    try:
        bot.play()
    except KeyboardInterrupt:
        print("Bot stopped.")

if __name__ == "__main__":
    main()
