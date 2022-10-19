from smtpClass import smtpClient
import sys
args = sys.argv[1:]

client = smtpClient(args[0],args[1])#'smtp.bgsu.edu', 25)
client.senderAndReceiver(args[2], args[3])#'xgschwi@bgsu.edu', 'xgschwi@bgsu.edu')
client.messageBody(args[4], args[5])#'Hi from yourself. HW4')
client.sendEmail()
client.endTheSession()
