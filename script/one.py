import yfinance as yf
import datetime as dt
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

pd1 = pd.read_csv(r'..\data\rbh.csv')

pd2 = pd1['Symbol']
# iterate over all the elements
#pd2 = pd1['Symbol']
#.tolist()
y = pd.DataFrame()
for counter, item in pd2.iteritems():
        x = yf.download(item, start = dt.datetime.today())
        x['Ticker'] = item
        y = y.append(x)




message = MIMEMultipart()
message["Subject"] = "Daily Stock Update"
message["From"] = 'sagardisa8@gmail.com'
message["To"] = 'sagardisa8@gmail.com'

html = """\
<html>
  <body>
    <p>Hi,<br>
       {0}
    </p>
  </body>
</html>
""".format(y.to_html())
# Turn these into plain/html MIMEText objects

part = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
message.attach(part)
fromaddr= 'sagardisa8@gmail.com'
toaddrs='sagardisa8@gmail.com'
username = 'sagardisa8@gmail.com'
password = '1234567XZ@'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, message.as_string())
server.quit()