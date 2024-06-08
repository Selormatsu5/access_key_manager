import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Change this to the appropriate port for your SMTP server
smtp_username = 'selormatsu5@gmail.com'
smtp_password = 'wlitlwfxeebagcgk'

# Sender and recipient email addresses
sender_email = 'selormatsu5@gmail.com'
recipient_email = 'selormkwame31@gmail.com'

# Email content
subject = 'Test Email'
body = 'This is a test email sent from Python.'

# Create a MIMEText object to represent the email body
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Connect to the SMTP server
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable TLS encryption
    server.login(smtp_username, smtp_password)
    print("Connected to SMTP server successfully.")

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully.")

except Exception as e:
    print(f"Error: Unable to send email. {e}")

finally:
    # Close the connection to the SMTP server
    server.quit()
