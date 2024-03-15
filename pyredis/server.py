import socket
from typing_extensions import Annotated
import typer


DEFAULT_PORT = 6379
DEFAULT_SERVER = "127.0.0.1"

def run_server(server: Annotated[str, typer.Argument()] = DEFAULT_SERVER,
         port: Annotated[int, typer.Argument()] = DEFAULT_PORT
         ):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((server, port))

    while True:
        server_socket.listen(1)
        print("Server is listening...")

        client_socket, address = server_socket.accept()
        print(f"Got a connection from {address}")

        data = client_socket.recv(1024)
        print(f"Recieved message: {data.decode('utf-8')}")

        client_socket.send(data)


if __name__ == '__main__':
    run_server()

