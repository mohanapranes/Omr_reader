import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class Email:
    def __init__(self):
        self.subject = "Mark-sheets"
        self.body = "Here is your mark sheet"
        self.sender_email = "omrproject.sheershare@gmail.com"
        self.password = "WxE6G8V8HJty7QL"
        self.message = MIMEMultipart()

    def multipart(self):
        self.message["From"] = self.sender_email
        self.message["To"] = ''
        self.message["Subject"] = self.subject
        self.message["Bcc"] = ''
        self.message.attach(MIMEText(self.body, "plain"))
    
    def attachSheet(self,sheet_path):
        message= self.message
        filename = sheet_path
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)
        return message
    
    def send(self,receiver_email,message):
        message["To"] = receiver_email
        message["Bcc"] = receiver_email
        text = message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, text)

email = Email()
email.multipart()
