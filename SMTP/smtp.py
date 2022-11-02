from smtpClass import smtpClient
import sys
args = sys.argv[1:]

# serverName, portNO, senderEmail, rcvEmail, emailText emailFileAttachement are all given as command line arguments
# smtp.py serverName portNo senderEmail rcvEmail emailText emailFileAttachment
# Example: python smtp.py smtp.bgsu.edu 25 xgschwi@bgsu.edu xgschwi@bgsu.edu "Hello there with attachment test HW4" results.txt

client = smtpClient(args[0],args[1]) #SMTP Server Name should be smtp.bgsu.edu with PortNo 25
client.senderAndReceiver(args[2], args[3]) # Sender and Receiver of emails
(status, err) = client.messageBody(args[4], args[5]) #Pass message content and attachment file location relative to call on functions

# if status == -1: #Error occurred with Attachment
#     print('Error in Message Body: ', err)
#     client.endTheSession()
# else: # Message and Attachment Ready
#     client.sendEmail()
#     client.endTheSession()
