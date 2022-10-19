from smtplib import SMTP # https://docs.python.org/3/library/smtplib.html

class smtpClient:	        #the return value & parameters are just informational - you decide what they need to be.
    message = ''
    server = None
    sender = ''
    receiver = ''
    
    def senderAndReceiver(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def messageBody(self, message):
        self.message = message

    def sendEmail(self):
        self.server.sendmail(from_addr=self.sender, to_addrs=[self.receiver])

    def endTheSession(self):
        self.server.quit()

    def __init__(self, serverMachine, portNumber):
        self.server = SMTP(host=serverMachine, port=portNumber)
        self.server.set_debuglevel(1)