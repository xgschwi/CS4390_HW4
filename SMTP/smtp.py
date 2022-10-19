from smtpClass import smtpClient

client = smtpClient('smtp.bgsu.edu', 25)
client.senderAndReceiver('xgschwi@bgsu.edu', 'xgschwi@bgsu.edu')
client.messageBody('Hi from yourself. HW4')
client.sendEmail()
client.endTheSession()
