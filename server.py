import pickle
from set import Game

import socket
import select

# Constants
FORMAT = "utf-8"
RECEIVE_COLOR = "\033[35m"
NORMAL_COLOR = "\033[32m"
ERROR_COLOR = "\033[31m"

# Create socket information
IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)

# Create the socket for clients to connecct to
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow PORT to be reused
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Make a point for clients to be able to connect with server_socket
server_socket.bind(ADDR)

# List of connected sockets, including server
sockets_list = [server_socket]

# dictionary of connected client sockets
clients = {}


def display(data, color=None):
    """
    Prints colored text to the console
    Parameters:
        data(string): message to be printed
        color(string): color for message to be printed in
    """
    if color is not None:
        print(color + data)
    else:
        print(NORMAL_COLOR + data)


def receive_package(active_client_socket):
    """
    Receives pickled object

    Receives message and returns it in two parts: header and data
    Parameters:
        active_client_socket(socket.socket): specific socket to receive message from
    Return: (Game) Game object
    """
    package = pickle.loads(active_client_socket.recv(4096 * 4))
    return package



def start():
    """
    Starts the server
    """
    username_list = []
    # Build game instance to pass to client
    static_game = Game()
    display("You have now set up the game on server", NORMAL_COLOR)
    # Get ready to accept clients
    server_socket.listen()
    display(f"Listening on {IP}")

    while True:
        read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)

        for specific_socket in read_sockets:
            # allow connections when checking the server
            if specific_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                # Receive game from client
                display("Receiving game package from client")
                game = pickle.loads(client_socket.recv(4096 * 4))
                display("Game package received from client")
                game_usernames = game.player_dict.keys() 
                for username in game_usernames:
                    # If server does not know about a player, add their name to a list
                    if username not in username_list:
                        username_list.append(username)
                    # If game doesn't know about a player, add it to the dictionary
                    if username not in static_game.player_dict.keys():
                        static_game.player_dict[username] = 0
                # Send game back to client
                client_socket.send(pickle.dumps(game))
                display("Package has been received and re-delivered")
                 
                sockets_list.append(client_socket)

            else:
                # This is the game package
                game = receive_package(specific_socket)

                if game == False:
                    display(f"Disconnected from {client_address}")
                    sockets_list.remove(specific_socket)
                    del clients[specific_socket]
                    continue
                username = game.username
                display("Accepting username: ", username)
                if username not in game.player_dict:
                    game.player_dict[username] = 0

                for client_socket in clients:
                    client_socket.send(game)

start()