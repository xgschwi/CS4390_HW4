import signal
from socket import *
from encodings import *
import sys, os
notFound404 = bytes('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>', 'utf-8')

def serverFileExists(filename):
     return os.path.isfile('./stored/' + filename + '.txt')

def getServerFile(filename):
    return open(os.path.join('./stored/', filename + '.txt'), 'r')


serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSock.bind(('localhost', 23456))

serverSock.listen(123)

while True:
    (clientSock, clientAddr) = serverSock.accept()
    req = clientSock.recv(1234).decode()

    print(req)

    url = '/'
    
    if len(req.split(' ')) > 1:
        url = req.split(' ')[1]

    if (url.__contains__('endconn')):
        clientSock.close()
        break
    
    fileLocation = url.split('/')[2].split('?', 1)[0]
    print(fileLocation)
    if (serverFileExists(fileLocation)):
        file = getServerFile(fileLocation)
        clientSock.send(bytes('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + file.read(), 'utf-8'))
        file.close()
    else:
        clientSock.send(notFound404)