import base64
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
    boundaryString = "====================bofbndnganry3532=="
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
    # Using MIME Library to understand format and printed results to base formatting off of
    # Sending RCPT TO
    # 250 2.1.5 Ok

    # Content-Type: multipart/mixed; boundary="===============0299229498347205954=="
    # MIME-Version: 1.0

    # --===============0299229498347205954==
    # Content-Type: text/plain; charset="us-ascii"
    # MIME-Version: 1.0
    # Content-Transfer-Encoding: 7bit

    # Hi there
    # --===============0299229498347205954==
    # Content-Type: application/octet-stream
    # MIME-Version: 1.0
    # Content-Transfer-Encoding: base64
    # Content-Disposition: attachment;filename=results.txt

    # fi9jczQzOTAvQ1M0MzkwX0hXNC9TTVRQJCBweXRob24gc210cC5weSBzbXRwLmJnc3UuZWR1IDI1
    def messageBody(self, message, attachment=None):
        messageMulti = 'Content-Type: multipart/mixed; boundary="' + self.boundaryString + '"\r\nMIME-Version: 1.0\r\n\r\n--' + self.boundaryString + '\r\n'#MIMEMultipart()
        #messageMulti.attach(MIMEText(message))
        messageMulti += 'Content-Type: text/plain; charset="us-ascii"\r\nMIME-Version: 1.0\r\n'
        messageMulti += message + '\r\n--' + self.boundaryString + '\r\n'

        # Add attachment
        messageMulti += 'Content-Type: application/octet-stream\r\nContent-Transfer-Encoding: base64 \r\n'
        messageMulti += 'Content-Disposition: attachment;\r\nfilename="' + attachment + '"\r\n\r\n'
        try:
            attachmentPart = None
            with open(attachment, 'rb') as a: # Read bytes of attachment
                attachmentPart = base64.b64encode(a.read()) # MIMEApplication takes raw bytes of data for attachment and defaults to recognize an octet stream
            # attachmentPart.add_header('Content-Disposition', 'attachment;filename=' + attachment) # Header for File Attachment
            print(attachmentPart)
            messageMulti += attachmentPart + '\r\n--' + self.boundaryString + '--\r\n\r\n.\r\n' 
            #messageMulti.attach(attachmentPart)
            #print(messageMulti.as_string())
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