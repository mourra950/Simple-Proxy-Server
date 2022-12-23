from socket import *
import sys

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server'
    )
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 5050))
tcpSerSock.listen(10)
# Fill in end.
while 1:
    # Start receiving data from the client
    print("\n\nReady to serve...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from:", addr)
    message = tcpCliSock.recv(1024)  # Fill in start. # Fill in end.
    #############################
    urlfile = open("urlfilter.txt", "r")
    urlblocked = urlfile.readlines()
    urlfile.close()
    ############################
    # Extract the filename from the given message
    if not (message.split()[1].decode("utf-8") in urlblocked) and message != "":
        filename = message.split()[1].decode("utf-8").rpartition("/")[2]
        fileExist = "false"
        filetouse = "./cache/" + filename

        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.readlines()
            fileExist = "true"
            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n")
            # Fill in start.
            print("Read from cache")
            for line in outputdata:
                tcpCliSock.send(line)
            f.close()

        # Error handling for file not found in cache
        except IOError:
            try:
                if fileExist == "false":
                    # Create a socket on the proxyserver
                    c = socket(AF_INET, SOCK_STREAM)  # Fill in start. # Fill in end.
                    hostn = message.split()[4].decode("utf-8")

                    # Connect to the socket to port 80
                    c.connect((hostn, 80))
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobjwrite = c.makefile("w", None)
                    # request
                    fileobjwrite.write(
                        "GET " + message.split()[1].decode("utf-8") + " HTTP/1.0\n\n"
                    )
                    fileobjwrite.close()
                    # Read the response into buffer
                    # read response
                    fileobj = c.makefile("rb", None)
                    buff = fileobj.readlines()
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    File = open("./cache/" + filename, "wb+")
                    for line in buff:
                        File.write(line)
                        tcpCliSock.send(line)
                    File.close()
                    c.close()
            except:
                print("Illegal")
    else:
        print("connection blocked")
        tcpCliSock.close()

else:
    ...
    # HTTP response message for file not found
    tcpCliSock.send("HTTP/1.0 404 sendError\r\n")
    tcpCliSock.send("Content-Type:text/html\r\n")
    # Close the client and the server sockets
    tcpCliSock.close()
    print("socket closed")
