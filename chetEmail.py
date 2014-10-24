from secrets import *

import smtplib

def send(emailTos, subject, text):

    emailTo = ','.join(emailTos)

    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (emailAddress, emailTo, subject, text)

    print 'SENDING EMAIL:'
    print ''
    print ''
    print message
    server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(emailAddress, emailPassword)
    server.sendmail(emailAddress, emailTo, message)
    server.close()
    print ''
    print ''
    print 'SENT'
