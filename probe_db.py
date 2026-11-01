import socket
try:
    with socket.create_connection(("127.0.0.1",15495),timeout=2):pass
except OSError:print("HOST DATABASE PORT CLOSED: 127.0.0.1:15495")
else:print("HOST DATABASE PORT REACHABLE: 127.0.0.1:15495")
