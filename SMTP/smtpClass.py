from smtplib import SMTP # https://docs.python.org/3/library/smtplib.html
    # attachments next https://docs.python.org/3/library/email.compat32-message.html#email.message.Message.add_header
    # https://docs.python.org/3/library/email.mime.html

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class smtpClient:	        #the return value & parameters are just informational - you decide what they need to be.
    message = ''
    server = None
    sender = ''
    receiver = ''
    
    def senderAndReceiver(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def messageBody(self, message, attachment=None):
        messageMulti = MIMEMultipart()
        messageMulti.attach(MIMEText(message))

        attachmentPart = None
        with open(attachment, 'rb') as a:
            attachmentPart = MIMEApplication(attachment.read())
        attachmentPart.add_header('Content-Disposition', 'attachment;filename=' + attachment)

        messageMulti.attach(attachmentPart)

        self.message = messageMulti.as_string()



    def sendEmail(self):
        self.server.sendmail(from_addr=self.sender, to_addrs=[self.receiver], msg=self.message)

    def endTheSession(self):
        self.server.quit()

    def __init__(self, serverMachine, portNumber):
        self.server = SMTP(host=serverMachine, port=portNumber)
        self.server.set_debuglevel(1)