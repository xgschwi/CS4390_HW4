from smtplib import SMTP # https://docs.python.org/3/library/smtplib.html
    # MIME Type message with attachment https://docs.python.org/3/library/email.compat32-message.html#email.message.Message.add_header
    # https://docs.python.org/3/library/email.mime.html
    # Header for file attachment https://blog.mailfence.com/email-header/
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class smtpClient:
    message = ''
    server = None
    sender = ''
    receiver = ''
    
    # Set the sender and receiver of emails
    def senderAndReceiver(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

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
            self.message = messageMulti.as_string()
        except Exception as e:
            return (-1, e)
        
        return (1, None)

    def sendEmail(self):
        self.server.sendmail(from_addr=self.sender, to_addrs=[self.receiver], msg=self.message)

    def endTheSession(self):
        self.server.quit()

    def __init__(self, serverMachine, portNumber):
        self.server = SMTP(host=serverMachine, port=portNumber)
        self.server.set_debuglevel(1)