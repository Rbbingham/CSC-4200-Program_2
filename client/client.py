import struct
from server.server import Server
from packet.packet import Packet
import socket


class Client(Server):
    def __init__(self, ip: str = "", port: int = 0, log: str = ""):
        super(Client, self).__init__(port, log)
        self.__ip: str = ip

    @property
    def ip(self) -> str:
        return self.__ip

    @ip.setter
    def ip(self, ip: str) -> None:
        self.__ip = ip

    def conserver(self):
        hello = Packet(17, 1, "Hello")
        hello_packet = hello.build()

        command = Packet(17, 2, "LIGHTON")
        command_packet_on = command.build()

        command.message = "LIGHTOFF"
        command_packet_off = command.build()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.__ip, super().port)
        sock.connect(server_address)

        sock.sendall(hello_packet)

        try:
            while True:
                data = sock.recv(struct.calcsize('!III'))
                version_raw, message_type_raw, length_raw = struct.unpack('!III', data)
                version = socket.ntohs(version_raw)
                message_type = socket.ntohs(message_type_raw)
                length = socket.ntohs(length_raw)
                print('version: {0:d} type: {1:d} length: {2:d}'.format(version, message_type, length))

                if version == 17:
                    print("VERSION ACCEPTED")
                else:
                    print("VERSION MISMATCH")

                message = sock.recv(length).decode()
                print("Message", message)

                if message_type == 1:
                    print("Sending command")
                    sock.sendall(command_packet_on)
                elif message_type == 2 and message == "SUCCESS":
                    print("Command Successful")
                    print('Closing socket')
                    break

        finally:
            sock.close()
