from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from repositories.db_service import DBService
import smtplib

class EmailManager:
    def send_notification(self, message: str, email: str):
        """
        Sends a notification message to the specified email.
        """
        # Email credentials and settings
        sender_email = "jlabs2519@gmail.com"  # Replace with your email
        receiver_email = email  # Replace with the receiver's email
        password = "uxnc zgiv vxwn moaa "  # Replace with your email password (or app-specific password)
        
        # Set up the SMTP server and port (for Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Port for TLS
 
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Test Email from Jlabs"
        
        # Body of the email
        body = "Hello, this is a test message!"
        
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            # Connect to the Gmail SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Start TLS encryption
            server.login(sender_email, password)  # Log in with the sender's credentials
        
            # Send the email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
        
            print("Email sent successfully!")
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            # Quit the SMTP server connection
            server.quit()

    #def send_report(self, report: 'ReportManager', email: str):
        """
        Sends a report to the specified email.
        """
        # Implementation for sending a report
        pass

