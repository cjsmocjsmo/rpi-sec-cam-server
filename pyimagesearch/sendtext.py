import smtplib 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import imghdr

class PiCamMail:
    def charlie(self, pimage):
        img_data = open(pimage, 'rb').read()
        email = "porthose.cjsmo.cjsmo@gmail.com"
        pas = "porthose01"
        sms_gateway = '9038201482@mymetropcs.com'
        smtp = "smtp.gmail.com" 
        port = 587
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(email, pas)
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sms_gateway
        msg['Subject'] = "PiCam\n"
        body = "Motion Has Been Detected\n"
        msg.attach(MIMEText(body, 'plain'))
        piimage = MIMEImage(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))
        msg.attach(piimage)
        sms = msg.as_string()
        server.sendmail(email,sms_gateway,sms)
        server.quit()



    def teresa(self, pimage):
        img_data = open(pimage, 'rb').read()
        email = "porthose.cjsmo.cjsmo@gmail.com"
        pas = "porthose01"
        sms_gateway = '9034366799@mymetropcs.com'
        smtp = "smtp.gmail.com" 
        port = 587
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(email, pas)
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sms_gateway
        msg['Subject'] = "PiCam\n"
        body = "Motion Has Been Detected\n This is a test"
        msg.attach(MIMEText(body, 'plain'))
        piimage = MIMEImage(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))
        msg.attach(piimage)
        sms = msg.as_string()
        server.sendmail(email,sms_gateway,sms)
        server.quit()

    def dylan(self, pimage):
        img_data = open(pimage, 'rb').read()
        email = "porthose.cjsmo.cjsmo@gmail.com"
        pas = "porthose01"
        sms_gateway = '3606201169@vtext.com'
        smtp = "smtp.gmail.com" 
        port = 587
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(email, pas)
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sms_gateway
        msg['Subject'] = "PiCam\n"
        body = "Motion detected\n "
        msg.attach(MIMEText(body, 'plain'))
        piimage = MIMEImage(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))
        msg.attach(piimage)
        sms = msg.as_string()
        server.sendmail(email,sms_gateway,sms)
        server.quit()

    def hill(self, pimage):
        img_data = open(pimage, 'rb').read()
        email = "porthose.cjsmo.cjsmo@gmail.com"
        pas = "porthose01"
        sms_gateway = '3606208524@vtext.com'
        smtp = "smtp.gmail.com" 
        port = 587
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(email, pas)
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sms_gateway
        msg['Subject'] = "PiCam\n"
        body = "Motion detected\n "
        msg.attach(MIMEText(body, 'plain'))
        piimage = MIMEImage(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))
        msg.attach(piimage)
        sms = msg.as_string()
        server.sendmail(email,sms_gateway,sms)
        server.quit()

    def amaya(self, pimage):
        img_data = open(pimage, 'rb').read()
        email = "porthose.cjsmo.cjsmo@gmail.com"
        pas = "porthose01"
        sms_gateway = '4254924983@txt.att.net'
        smtp = "smtp.gmail.com" 
        port = 587
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(email, pas)
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sms_gateway
        msg['Subject'] = "PiCam\n"
        body = "Motion detected\n "
        msg.attach(MIMEText(body, 'plain'))
        piimage = MIMEImage(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))
        msg.attach(piimage)
        sms = msg.as_string()
        server.sendmail(email,sms_gateway,sms)
        server.quit()
# charlie()
# teresa()
# # dylan()