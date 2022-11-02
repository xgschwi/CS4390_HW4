import base64
import os
from socket import *

# https://www.rfc-editor.org/rfc/rfc821

class smtpClient:
    message = ''
    server = None
    sender = ''
    receiver = ''
    boundaryString = "====================boundaryString=="

    # Set the sender and receiver of emails
    def senderAndReceiver(self, sender, receiver):
        send = "MAIL FROM:" + sender + "\r\n"
        # MAIL FROM and RCPT TO
        print(send)

        self.server.send("MAIL FROM:" + sender + "\r\n")
        recv = self.server.recv(1024)

        print(recv)
        if ("250" not in str(recv)):
            return (-1, "Error setting sender")

        send = "RCPT TO:" + receiver + "\r\n"
        print(send)

        self.server.send(send)
        recv = self.server.recv(1024)

        print(recv)

        if ("250" not in str(recv)):
            return (-1, "Error setting recipient")
        self.sender = sender
        self.receiver = receiver
        return (1, None)


    
    # Additioanlly used this resource to understand MIME Formatting: http://www.gentle.it/alvise/smtp.htm
    # Set the message body, which is a MIME type of multiple parts, with message body and attachment
    # results.txt contains MIME Library usage with smtplib that also helped with formulating the body of the data
    def messageBody(self, message, attachment=None):
        messageMulti = 'Content-Type: multipart/mixed; boundary="' + self.boundaryString + '"\r\nMIME-Version: 1.0\r\n\r\n--' + self.boundaryString + '\r\n'#MIMEMultipart()

        messageMulti += 'Content-Type: text/plain; charset="us-ascii"\r\nMIME-Version: 1.0\r\n\r\n'
        messageMulti += message + '\r\n--' + self.boundaryString + '\r\n'

        # Add attachment
        messageMulti += 'Content-Type: application/octet-stream\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: base64\r\n'
        messageMulti += 'Content-Disposition: attachment;filename="' + os.path.basename(os.path.normpath(attachment)) + '"\r\n\r\n'
        try:
            attachmentPart = None
            with open(attachment, 'rb') as a: # Read bytes of attachment
                attachmentPart = base64.b64encode(a.read()) # Get base64 encoding of file contents

            messageMulti += attachmentPart + '\r\n--' + self.boundaryString + '--\r\n.\r\n' 
            self.message = messageMulti
        except Exception as e:
             return (-1, e)
        
        return (1, None)

    def sendEmail(self):
        print("DATA")
        self.server.send("DATA\r\n")
        recv = self.server.recv(1024)
        print(recv)
        
        send = "From: " + self.sender + "\r\n"
        send += "To: " + self.receiver + "\r\n"
        send += "Subject: HW4\r\n"
        send += self.message

        print(send)
        self.server.send(send)

        recv = self.server.recv(1024)
        print(recv)

    def endTheSession(self):
        print("QUIT")
        self.server.send("QUIT\r\n")
        recv = self.server.recv(1024)
        print(recv)

    def __init__(self, serverMachine, portNumber):
        self.server = socket(AF_INET, SOCK_STREAM)
        print("Connecting to " + serverMachine + " via port number " + portNumber)
        self.server.connect((serverMachine, int(portNumber))) # one argument as tuple
        recv = self.server.recv(1024)

        print(recv)

        # Connecting Use HELO command 3.5. The first command in a session must be the HELO command
        send = "HELO " + gethostname() + "\r\n"
        print(send)
        self.server.send(send)
        
        recv = self.server.recv(1024)
        print(recv)

        #   The following are the SMTP commands:

        #     HELO <SP> <domain> <CRLF>

        #     MAIL <SP> FROM:<reverse-path> <CRLF>

        #     RCPT <SP> TO:<forward-path> <CRLF>

        #     DATA <CRLF>

        #     RSET <CRLF>

        #     SEND <SP> FROM:<reverse-path> <CRLF>

        #     SOML <SP> FROM:<reverse-path> <CRLF>

        #     SAML <SP> FROM:<reverse-path> <CRLF>

        #     VRFY <SP> <string> <CRLF>

        #     EXPN <SP> <string> <CRLF>

        #     HELP [<SP> <string>] <CRLF>

        #     NOOP <CRLF>

        #     QUIT <CRLF>

        #     TURN <CRLF>