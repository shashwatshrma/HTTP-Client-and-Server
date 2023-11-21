import socket
import sys
import os

port_number = int(28333)

# setting the variables from the command line arguments
if len(sys.argv) == 2:
    port_number = int(sys.argv[1])

# making a new socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the specified port number and start listening to it
s.bind(("", port_number))
s.listen()

mime = {
    ".txt": "text/plain",
    ".css": "text/css",
    ".html": "text/html",
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpg",
    ".png": "image/png",
    ".js": "application/js",
    ".json": "application/json",
    ".pdf": "application/pdf",
}

for i in range(0,10):
    new_connection = s.accept()
    new_socket = new_connection[0]

    request_data = ""
    while True:
        temp = new_socket.recv(4096)
        request_data += temp.decode("ISO-8859-1")
        if request_data.find("\r\n\r\n"):
            break
    
    if request_data == "":
        response = (
            protocol
            + " 400 Bad Request\r\nContent-Type: text/plain\r\nContent-Length: 15\r\nConnection: close\r\n\r\n404 not found\r\n"
        )
    else:
        print("IP address connected: " + new_connection[-1][0])
        print("Port number connected: " + str(new_connection[-1][1]))
        print("Request method: " + request_data.split(" ")[0] + "\n")
        print(request_data)

        first_line = request_data.split("\r\n")[0]
        method = first_line.split(" ")[0]
        file_name = first_line.split(" ")[1].split("/")[-1]
        exten = os.path.splitext(file_name)[1]
        protocol = first_line.split(" ")[2]

        try:
            with open(file_name, "rb") as fp:
                data = fp.read()
            response = (
                protocol
                + " 200 OK\r\nContent-Type: "
                + mime[exten]
                + "\r\nContent-Length: "
                + str(len(data))
                + "\r\nConnection: close\r\n\r\n"
                + data.decode("utf-8")
                + "\r\n"
            )
        except:
            response = (
                protocol
                + " 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found\r\n"
            )

    new_socket.send(response.encode("ISO-8859-1"))
    new_socket.close()

s.close()