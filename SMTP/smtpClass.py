from smtplib import SMTP # https://docs.python.org/3/library/smtplib.html
    # MIME Type message with attachment https://docs.python.org/3/library/email.compat32-message.html#email.message.Message.add_header
    # https://docs.python.org/3/library/email.mime.html
    # Header for file attachment https://blog.mailfence.com/email-header/
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from socket import *

# https://www.rfc-editor.org/rfc/rfc821

class smtpClient:
    message = ''
    server = None
    sender = ''
    receiver = ''
    
    # Set the sender and receiver of emails
    def senderAndReceiver(self, sender, receiver):
        # MAIL FROM and RCPT TO
        print("Sending MAIL FROM")
        self.server.send("MAIL FROM:" + sender + "\r\n")
        recv = self.server.recv(1024)
        print(recv)
        if ("250" not in str(recv)):
            return (-1, "Error setting sender")

        print("Sending RCPT TO")
        self.server.send("RCPT TO:" + receiver + "\r\n")
        recv = self.server.recv(1024)
        print(recv)

        if ("250" not in str(recv)):
            return (-1, "Error setting recipient")
        # self.sender = sender
        # self.receiver = receiver


    # Set the message body, which is a MIME type of multiple parts, with message body and attachment
    def messageBody(self, message, attachment=None):
        messageMulti = MIMEMultipart()
        messageMulti.attach(MIMEText(message))

        try:
            attachmentPart = None
            with open(attachment, 'rb') as a: # Read bytes of attachment
                attachmentPart = MIMEApplication(a.read()) # MIMEApplication takes raw bytes of data for attachment and defaults to recognize an octet stream
            attachmentPart.add_header('Content-Disposition', 'attachment;filename=' + attachment) # Header for File Attachment

            messageMulti.attach(attachmentPart)
            print(messageMulti.as_string())
        #     self.message = messageMulti.as_string()
        except Exception as e:
             return (-1, e)
        
        return (1, None)

    #def sendEmail(self):
       # self.server.sendmail(from_addr=self.sender, to_addrs=[self.receiver], msg=self.message)

    #def endTheSession(self):
        #self.server.quit()

    def __init__(self, serverMachine, portNumber):
        self.server = socket(AF_INET, SOCK_STREAM)
        print("Connecting to " + serverMachine + " via port number " + portNumber)
        self.server.connect((serverMachine, int(portNumber))) # one argument as tuple
        recv = self.server.recv(1024)

        print(recv)

        # Connecting Use HELO command 3.5. The first command in a session must be the HELO command
        print("Sending HELO")
        self.server.send("HELO " + gethostname() + "\r\n")
        
        recv = self.server.recv(1024)
        print(recv)

        #self.server = SMTP(host=serverMachine, port=portNumber)
        #self.server.set_debuglevel(1)



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