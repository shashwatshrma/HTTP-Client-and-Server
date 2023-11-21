import socket
import sys

host_name = str()
port_number = int(80)

# setting the variables from the command line arguments
if len(sys.argv) == 3:
    host_name = sys.argv[1]
    port_number = int(sys.argv[2])
elif len(sys.argv) == 2:
    host_name = sys.argv[1]
else:
    print("Please provide a url")
    exit(0)

# making a new socket
s = socket.socket()
s.connect((host_name, port_number))

# making the http request and sending it
request = "GET / HTTP/1.1\r\nHost: " + host_name + "\r\nConnection: close\r\n\r\n"
request = request.encode("ISO-8859-1")
s.sendall(request)

# getting the response data
response_data = ""
while True:
    temp = s.recv(4096)
    if len(temp) == 0:
        break
    response_data += temp.decode("ISO-8859-1")

print(response_data)

s.close()
