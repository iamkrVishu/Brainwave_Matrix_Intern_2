import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message, to_addr):
    try:
        from_addr = "your_email@gmail.com"  # Change this to your email
        password = "your_email_password"  # Use app password, NOT your main password

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()

        print(f"✅ Email sent successfully to {to_addr}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False