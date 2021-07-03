from set import Game
import arcade

import threading

import socket
import pickle

# Constants
FORMAT = "utf-8"
RECEIVE_COLOR = "\033[35m"
NORMAL_COLOR = "\033[32m"
ERROR_COLOR = "\033[31m"

# IP address of this computer
IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)

def display(data, color=None):
    """
    Prints colored text to the console
    Parameters:
        data(string): message to be printed
        color(string): color for message to be printed in
    """
    if color is not None:
        print(color + data + NORMAL_COLOR)
    else:
        print(NORMAL_COLOR + data)


# Create Client object
class Client():
    def __init__(self):
        # define username after connecting to server and getting game package
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.client_socket.setblocking(True)

        # Create game instance and pass in username
        # Game instance will be defined by server and passed to the client
        self.game = Game()
        self.game.username = input("Username: ")
        if self.game.username not in self.game.player_dict.keys():
            self.game.player_dict[self.game.username] = 0
        
    

    def setup_game(self):
        # Client should send game first, then receive game from server
        display("Sending game package to server")
        self.send_game_package(self.game)
        display("Game package has been sent to server")


        display("Receiving game package")
        self.game = self.receive_game_package()
        display("Game package received")
        self.window = self.game.Display()
        
        self.window.setup()
        self.send_thread = threading.Thread(None, self.check_for_send_flag, )
        self.run_game()


    def send_game_package(self, game):
        """Packages and sends game"""
        self.client_socket.send(pickle.dumps(game))
    

    def receive_game_package(self):
        """Receives the game package"""
        package = pickle.loads(self.client_socket.recv(4096 * 4))
        return package


    def run_game(self):
        """Starts the send thread and starts the game"""
        self.send_thread.start()
        arcade.run()
    

    def check_for_send_flag(self):
        """Chacks to see if game should be sent to server"""
        while self.game.send_flag == True:
            self.send_game_package(game=self.game)
            

if __name__ == "__main__":
    client = Client()
    client.setup_game()
    client.run_game()
