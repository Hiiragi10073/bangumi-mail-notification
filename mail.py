from loadYaml import loadYaml
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

config = loadYaml('config.yaml')
emailConfig = config.get('email')

sender = emailConfig.get('from')
user = emailConfig.get('user')
passwd = emailConfig.get('passwd')
receivers =  emailConfig.get('to')

receiversEmailAddress = []
receiversAddr = []
for recipient in receivers:
  receiversEmailAddress.append(recipient[1])
  receiversAddr.append(formataddr(recipient))

def send(subject, content, sendAll):
  message = MIMEMultipart('related')
  message['From'] = formataddr(sender)
  if sendAll:
    message['To'] = ", ".join(receiversAddr)
  else:
    message['To'] = receiversAddr[0]


  message['Subject'] = subject

  msgAlternative = MIMEMultipart('alternative')
  message.attach(msgAlternative)

  msgAlternative.attach(MIMEText(content, 'html', 'utf-8'))

  server = smtplib.SMTP_SSL('smtp.163.com', 465)
  server.login(user, passwd)

  if sendAll:
    server.sendmail(user, receiversEmailAddress, message.as_string())
  else:
    server.sendmail(user, [receiversEmailAddress[0]], message.as_string())

  server.quit()
  print('邮件发送成功')