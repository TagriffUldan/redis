import typer
from typing_extensions import Annotated
import socket
from data_types import encode_message, Array, BulkString, RespDataType
from protocol_handler import extract_frame_from_buffer

DEFAULT_PORT = 6379
DEFAULT_SERVER = "127.0.0.1"
RECV_SIZE = 1024

def encode_command(command: str) -> RespDataType:
    return Array([BulkString(word) for word in command.split()])


def main(server: Annotated[str, typer.Argument()] = DEFAULT_SERVER,
         port: Annotated[int, typer.Argument()] = DEFAULT_PORT
         ):
    
    with socket.socket() as client_socket:
        client_socket.connect((server, port))


        while True:
            command = input(f"{server}:{port} ")
            encoded_message = encode_message(encode_command(command))

            if command.lower() == 'quit':
                break
            else:
                client_socket.send(encoded_message)  
                
                buffer = bytearray()
                data = client_socket.recv(RECV_SIZE)
                buffer.extend(data)
                print(buffer)

                # encoded_message = encode_message(encode_command(command))
                # client_socket.send(encoded_message)  
                
                # buffer = bytearray()
                # data = client_socket.recv(RECV_SIZE)
                # buffer.extend(data)
                
                # frame, frame_size = extract_frame_from_buffer(buffer)
                
                # while True:
                #     if frame:
                #         buffer = buffer[frame_size:]
                #         if isinstance(frame, Array):
                #             for count, item in enumerate(frame.data):
                #                 print(f'{count + 1}) "{item.data}"')
                #         else:
                #             print(frame.data)
                #         break


        
if __name__ == '__main__':
    typer.run(main)