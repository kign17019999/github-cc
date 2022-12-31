import socket

class MasterWorker:
    def __init__(self, connections, master=True):
        self.connections = []
        self.sockets = []
        self.connection_available = 0
        self.timeout = 0.5
        if master:
            for connection in connections:
                ip, port = connection
                self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                self.sockets[-1].bind((ip, port))
                print(f'Listening on {ip}:{port}')
                self.sockets[-1].listen()
        else:
            for connection in connections:
                ip, port = connection
                self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                result = self.sockets[-1].connect_ex((ip, port))
                print(f'Connection result {result}')
                while result != 0:
                    result = self.sockets[-1].connect_ex((ip, port))
                    print(f'Connection result {result}')
                self.sockets[-1].settimeout(self.timeout)

    def accept_connections(self, connection_index = -1):
        conn, addr = self.sockets[connection_index].accept()
        print(f"Connection from: {addr}")
        self.sockets[connection_index] = conn
        self.sockets[connection_index].settimeout(self.timeout)
        
    def add_connection(self, connections, master=True):
        master_worker = MasterWorker(connections, master=master)
        for socket in master_worker.sockets:
            self.sockets.append(socket)

    def send(self, message, connection_index=0):
        self.sockets[connection_index].send(message)

    def get(self, length, connection_index=0):
        try:
            message = self.sockets[connection_index].recv(length)
            return message
        except socket.timeout:
            return b""
    
    def send_withHeader(self, message, header_byte, connection_index=0):
        message_len = len(message)
        header = (message_len).to_bytes(header_byte, byteorder="big") + message
        self.sockets[connection_index].send(header)
    
    def get_withHeader(self, header_byte, length, connection_index=0):
        try:
            header = self.sockets[connection_index].recv(header_byte)
            message_len = int.from_bytes(header, byteorder="big")
            message = b""
            while len(message) < message_len:
                # Receive up to length bytes at a time
                if message_len - len(message) > length:
                    message_chunk = self.sockets[connection_index].recv(length)
                else:
                    message_chunk = self.sockets[connection_index].recv(message_len - len(message))

                # Append the received data to the message
                message += message_chunk
            return message
        except socket.timeout:
            return b""

    def close(self, connection_index=0):
        self.sockets[connection_index].close()

    def close_all(self):
        for connection in self.sockets:
            connection.close()
    
    def display_connections(self):
        self.connection_available = len(self.sockets)
        print("Current connections:")
        for i in range(len(self.sockets)):
            try:
                print(f"{i}: local {self.sockets[i].getsockname()[0]}:{self.sockets[i].getsockname()[1]} | remote {self.sockets[i].getpeername()[0]}:{self.sockets[i].getpeername()[1]}")
            except:
                try:
                    self.connection_available -=1
                    print(f"{i}: local {self.sockets[i].getsockname()[0]}:{self.sockets[i].getsockname()[1]} | no connection")
                except:
                    print('no any socket')
                    
        return self.connection_available