from smtpClass import smtpClient
import sys
args = sys.argv[1:]

client = smtpClient(args[0],args[1]) #SMTP Server Name should be smtp.bgsu.edu with PortNo 25
client.senderAndReceiver(args[2], args[3]) # Sender and Receiver of emails
(status, err) = client.messageBody(args[4], args[5]) #Pass message content and attachment file location relative to call on functions

if status == -1: #Error occurred with Attachment
    print('Error in Message Body: ', err)
    client.endTheSession()
else: # Message and Attachment Ready
    client.sendEmail()
    client.endTheSession()
