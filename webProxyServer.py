from socket import *
import os

# Create a server socket, bind it to a port, and start listening
proxySerSock = socket(AF_INET, SOCK_STREAM)
proxySerSock.bind(("", 8080))
proxySerSock.listen(5)

while 1:
    print('Ready to serve...')
    # Accept connection from clients
    proxyCliSock, addr = proxySerSock.accept()
    print('Received a connection from:', addr)

    # Get the HTTP request from the client
    message = proxyCliSock.recv(1024).decode()
    print(message)

    # If the message is not a GET request, send a 400 Bad Request response
    if not message.startswith("GET"):
        print("Message is not a GET request")
        proxyCliSock.send("HTTP/1.0 400 Bad Request\r\nConnection: close\r\n\r\n".encode())
        proxyCliSock.close()
        continue

    # Extract the pathname and hostname from the message
    slashPlusUrl = message.split()[1]
    url = slashPlusUrl.partition("/")[2]
    hostn = url.split('/')[0]
    pathname = '/'.join(url.split('/')[1:])
    pathname = "/" + pathname

    # Remove "www." from the hostname if it starts with "www."
    if hostn.startswith("www."):
        hostn = hostn.replace("www.", "", 1)

    print("pathname:", pathname)
    print("hostname:", hostn)

    fileExist = "false"

    # Construct the directory path for caching
    directory = f"./cache/{hostn}{pathname}"

    try:
        # Check if the file exists in the cache
        f = open(directory, "rb")
        object = f.read()

        # Send HTTP response header and object
        proxyCliSock.send("HTTP/1.0 200 OK\r\nConnection: close\r\n\r\n".encode())
        proxyCliSock.send(object)

        fileExist = "true"
        print('Read from cache')

        # Close socket and file
        proxyCliSock.close()
        f.close()

    except IOError:  # File not found in cache
        if fileExist == "false":
            # Create a socket to connect to the original server on port 80
            proxyAsClientSocket = socket(AF_INET, SOCK_STREAM)
            proxyAsClientSocket.connect((hostn, 80))

            # Create a GET request message and send it to the server
            request = f"GET {pathname} HTTP/1.0\r\nHost: {hostn}\r\nConnection: close\r\n\r\n"
            proxyAsClientSocket.send(request.encode())

            # Receive data from the web server
            total_response = b''
            while True:
                response_chunk = proxyAsClientSocket.recv(4096)
                if not response_chunk:
                    break
                total_response += response_chunk

            # Separate header and object
            response_header, response_object = total_response.split(b'\r\n\r\n', 1)

            if b'200 OK' in response_header:
                # Create the directory and write the object to the file
                os.makedirs(os.path.dirname(directory), exist_ok=True)
                with open(directory, "wb") as f:
                    f.write(response_object)

                # Send the response header and object to the client
                proxyCliSock.send(response_header + b'\r\n\r\n')
                proxyCliSock.send(response_object)
            else:
                # Send a 400 Bad Request response if not 200 OK
                proxyCliSock.send("HTTP/1.0 400 Bad Request\r\nConnection: close\r\n\r\n".encode())

            # Close socket between proxy and origin server
            proxyAsClientSocket.close()
        else:
            break
    except Exception as e:
        print("An Exception Occurred:", e)
    finally:
        # Close socket between proxy and client
        proxyCliSock.close()
    break  # Remove "break" to keep the proxy running for multiple requests

# Close the main proxy listening socket
proxySerSock.close()
print("Finish")
