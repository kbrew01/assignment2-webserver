# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)
  #Prepare a server socket
  serverSocket.bind(("", port))
  serverSocket.listen(5)

  print('the web server is up on port:',port)

  while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:

      try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        
        #Send one HTTP header line into socket.
        connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")



        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
          connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
      except IOError:
        #Send response message for file not found (404)
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send(b"<html><head></head><body>404 not found</body></html>")




        #Close client socket
        connectionSocket.close()



    except (ConnectionResetError, BrokenPipeError):
      pass

  serverSocket.close()
  sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)
