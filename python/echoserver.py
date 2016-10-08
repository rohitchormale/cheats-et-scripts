#!/usr/bin/env python

"""
Simple TCP echo server
"""


import socket
import threading
import sys


def validate(port, interface):
    """Validate port & interface
    return boolean True/False"""
    try:
        port = int(port)
        if not(1025 <= int(port) <= 65535):
            raise ValueError
        if not interface.lower() == "localhost":
            socket.inet_aton(interface)
    except (ValueError, socket.error) as e:
        print e
        return False
    return True

def start_echo_server(port, interface):
    def handle_client(client):
        buffer = client.recv(1042)
        if buffer:
            client.send(buffer)
        client.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((interface, port))
    server_socket.listen(5)
    print("Server started at %s:%s" %(interface, port))
    
    while True:
        client_socket, addr = server_socket.accept()
        print("Got a connection | %s:%s" %(addr[0], addr[1]))
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


def start_echo_service(port, interface):
    import daemon
    with daemon.DaemonContext():
        start_echo_server(port, interface)


def main():
    # Take args from user
    interface = raw_input("Enter an interface (default 127.0.0.1): ")
    interface = interface.strip()
    if interface == "":
        interface = "127.0.0.1"

    port = raw_input("Enter a port (default 9999): ")
    port = port.strip()
    if port == "": 
        port = 9999

    is_daemon = raw_input("Run as daemon? (default: no): ")
    is_daemon = is_daemon.strip()

    # Validate args 
    if validate(port, interface):
        if is_daemon.lower() in ("y", "yes"):
            start_echo_service(int(port), interface)
        else:
            start_echo_server(int(port), interface)
    else:
        print("Invalid arguments. Exiting !!!")
        sys.exit(1)


if __name__ == '__main__':
    main()


