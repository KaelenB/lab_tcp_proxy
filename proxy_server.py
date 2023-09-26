import socket
from threading import Thread


BYTES_TO_READ = 4096
HOST = '127.0.0.1'
PORT = 8080



def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)

        data = s.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0:
            data = s.recv(BYTES_TO_READ)
            result += data
        return result
    

def handle_connection(conn, addr):
    with conn:
        print(f"Conntected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data

        respose = send_request("www.google.com", 80, request)
        conn.sendall(respose)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)
        conn, addr = s.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)

        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()



start_threaded_server()