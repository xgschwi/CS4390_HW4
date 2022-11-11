from socket import *
from encodings import *
import os

invalidRequest = bytes('HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<html><body><h1>400 Bad Request</h1></body></html>', 'utf-8') # The request is malformed - i.e. does not reference the server
notFound404 = bytes('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>', 'utf-8') # File not found on server nor proxy
unauth401 = bytes('HTTP/1.1 401 Unauthorized\r\nContent-Type: text/html\r\n\r\n<html><body><h1>401 Unauthorized</h1></body></html>', 'utf-8') # Request does not contain authorization details
forbidden403 = bytes('HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<html><body><h1>403 Forbidden</h1></body></html>', 'utf-8') # Request has invalid authorization credentials

# clear cache on each run
for f in os.listdir('./cached'):
    os.remove(os.path.join('./cached/', f))

def cacheFile(filename, contents):
    with open(os.path.join('./cached/', filename + '.txt'), 'w') as f:
        f.write(contents)
        f.close()
        print('File ' + filename + ' is cached!')

def cacheFileExists(filename):
    return os.path.isfile('./cached/' + filename + '.txt')

def getCacheFile(filename):
    return open(os.path.join('./cached/', filename + '.txt'), 'r')

def authorizeUser(url):
    auth = url.split('?auth=')[1]
    if (auth == 'password'): return True
    else: return False


proxySock = socket(AF_INET, SOCK_STREAM)
proxySock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

proxySock.bind(('localhost', 12345))

proxySock.listen(123)

try:       
    while True:
        (clientSock, clientAddr) = proxySock.accept()
        req = clientSock.recv(1234).decode()

        print(req)

        url = '/'
        
        if len(req.split(' ')) > 1:
            url = req.split(' ')[1]
            
        if (url.__contains__('/endconn')):
            clientSock.close()
            serverSock.shutdown(SHUT_RDWR)
            break

        if (not url.__contains__('localhost:23456')):
            print(invalidRequest.decode())
            clientSock.send(invalidRequest)
        elif (not url.__contains__('?auth=')):
            print(unauth401.decode())
            clientSock.send(unauth401)
        else:
            if (not authorizeUser(url)):
                print(forbidden403.decode())
                clientSock.send(forbidden403)
            else:
                fileLocation = url.split('/')[2].split('?', 1)[0]
                if (cacheFileExists(fileLocation)):
                    print('This file is cached, sending now')
                    file = getCacheFile(fileLocation)
                    fileContents = file.read()
                    print('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><p>Here is your cached file:</p><p>' + fileContents + '</p></body></html>')
                    clientSock.send(bytes('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><p>Here is your cached file:</p><p>' + fileContents + '</p></body></html>', 'utf-8'))
                    file.close()
                else:
                    serverSock = socket(AF_INET, SOCK_STREAM)
                    serverSock.connect(('localhost', 23456))
                    print('GET ' + url + ' HTTP/1.1')
                    serverSock.send(bytes('GET ' + url + ' HTTP/1.1', 'utf-8'))
                    sReq = serverSock.recv(1234).decode()
                    print(sReq)
                    sUrl = sReq.split(' ')[1]

                    if sUrl == '404':
                        print(notFound404.decode())
                        clientSock.send(notFound404)
                    else:
                        cacheFile(fileLocation, sReq.split('\r\n')[3])
                        print('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body>' + sReq.split('\r\n')[3] + '</body></html>')
                        clientSock.send(bytes('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body>' + sReq.split('\r\n')[3] + '</body></html>', 'utf-8'))
                    serverSock.close()

        
except:
    proxySock.close()