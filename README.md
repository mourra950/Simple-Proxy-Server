# Simple Proxy Server

## Project Description

This is a simple HTTP proxy server implemented in Python. It listens for incoming connections on a specified port and receives HTTP request messages from clients. If the requested URL is not in a list of blocked URLs, the server attempts to retrieve the requested file from the cache directory. If the file is found in the cache, it is sent to the client. If the file is not found in the cache, the server creates a socket and connects to the host specified in the request message, sends an HTTP request for the file, and receives the response. The response is then stored in a cache file and also sent to the client. If an error occurs while trying to retrieve the file, an HTTP error message is sent to the client.

## Dependencies

Nothing is needed to be downloaded as the socket is integrated into python.

## Usage

in a terminal execute the following code while replacing the IP address with a suitable IP for the proxy server.

```ssh
python skeleton.py [ipAdrress]
```

then activate the proxy server in the setting of the browser or the operating system to work.

## Code Explanation

### Server Initialization

```python
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
```

### Server storing messages

```python
# Start receiving data from the client
print("\n\nReady to serve...")
tcpCliSock, addr = tcpSerSock.accept()
print("Received a connection from:", addr)
message = tcpCliSock.recv(1024)
```

### Server reading the filtered sites

```python
urlfile = open("urlfilter.txt", "r")
urlblocked = urlfile.readlines()
urlfile.close()
```

### Check for messages and start proccessing

```python
if message:
    # Extract the filename from the given message
    filename = message.split()[1].decode("utf-8").rpartition("/")[2]
    #check if the url is block if not keep going
    if not (message.split()[1].decode("utf-8") in urlblocked) :
        fileExist = "false"
        filetouse = "\\cache\\" + filename
```

### Check in the cache folder if found send response

```python
try:
# Check wether the file exist in the cache if not found go to exception handling
    f = open(filetouse[1:], "rb")
    outputdata = f.readlines()
    print("Read from cache")
    fileExist = "true"
    # ProxyServer finds a cache hit and generates a response message
    tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
    tcpCliSock.send(b"Content-Type:text/html\r\n")
    #send data to user
    for line in outputdata:
        tcpCliSock.send(line)
    f.close()
```

### Exception handling and cache retrieving

```python
# Error handling for file not found in cache
except IOError:
    try:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            # extracting the hostname from the message
            hostn = message.split()[4].decode("utf-8")
            # Connect to the socket to port 80
            c.connect((hostn, 80))
            # Create a temporary file on this socket and ask port 80 for the file requested by the client
            fileobjwrite = c.makefile("w", None)
            #format the request and send it
            fileobjwrite.write("GET " + message.split([1].decode("utf-8") + " HTTP/1.0\n\n")
            fileobjwrite.close()
            # Read the response into buffer
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
#if any error occured during the proccess mostly will be the website we trying to access is not an html file
    except:
        print("Illegal")
else:
#closing the tcp socket
tcpCliSock.close()

```

# Notes

This proxy server is intended for educational and demonstration purposes only and should not be used in a production environment. It has not been thoroughly tested and may contain bugs or security vulnerabilities.