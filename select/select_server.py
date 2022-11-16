# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select


def run_server(port):

    # Make the server socket and bind it to the port
    servers_socket = socket.socket()
    servers_socket.bind(("", port))
    servers_socket.listen()

    # listener socket
    listener = [servers_socket]

    # loop forever
    while True:

        # call select(), get sockets that are ready-to-read
        ready_to_read, _, _ = select.select(listener, [], [])

        # for each socket that is ready-to-read
        for s in ready_to_read:

            # if the socket is the listener socket, then accept the connection
            if s is servers_socket:
                clients_socket, _ = servers_socket.accept()
                print_client_connection(clients_socket)
                listener.append(clients_socket)

            # else it is just a regular socket
            else:
                contents = s.recv(4096)

                # if no content, client disconnected
                if not contents:
                    print_client_disconnection(s)
                    s.close()
                    listener.remove(s)
                else:
                    print_message(s, contents)

def print_client_connection(clients_socket):
    print(f"{clients_socket.getpeername()}: connected")

def print_client_disconnection(clients_socket):
    print(f"{clients_socket.getpeername()}: disconnected")

def print_message(clients_socket, contents):
    print(f"{clients_socket.getpeername()}: {len(contents)} bytes: {contents}")

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
