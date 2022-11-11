import signal
from socket import *
from encodings import *
import sys, os
notFound404 = bytes('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>', 'utf-8')
invalidRequest = bytes('HTTP/1.1 400 Bad Request', 'utf-8')

# clear cache on each run
for f in os.listdir('./cached'):
    os.remove(os.path.join('./cached', f))

def cacheFile(filename, contents):
    with open(os.path.join('./cached', filename + 'txt'), 'w') as f:
        f.write(contents)
        f.close()

def cacheFileExists(filename):
    return os.path.isfile('./cached' + filename + '.txt')

def getCacheFile(filename):
    return open(os.path.join('./cached', filename + 'txt'), 'r')



proxySock = socket(AF_INET, SOCK_STREAM)
proxySock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# def shutdown(sig, var):
#     try:

#         serverSock.shutdown(SHUT_RDWR)
#         sys.exit(1)
#     except:
#         pass

# signal.signal(signal.SIGINT, shutdown)

proxySock.bind(('localhost', 12345))

proxySock.listen(123)

while True:
    (clientSock, clientAddr) = proxySock.accept()
    req = clientSock.recv(1234).decode()

    # if not req:
    #     break

    print(req)

    url = '/'
    
    if len(req.split(' ')) > 1:
        url = req.split(' ')[1]

    print(url)
    if (url == '/'):
        clientSock.send(notFound404)
        
    if (url == '/endconn'):
        clientSock.close()
        break

    if (not url.__contains__('localhost:23456')):
        clientSock.send(invalidRequest)
    else:
        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.connect(('localhost', 23456))
        serverSock.send(bytes('GET ' + url + ' HTTP/1.1', 'utf-8'))

    
