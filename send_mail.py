import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


load_dotenv()


def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    user = os.environ.get("MAIL_USER")
    password = os.environ.get("MAIL_PASSWORD")

    with smtplib.SMTP(smtp_server, port) as server:
        sender = "lfcamachodev@gmail.com"
        receiver = "luisfernandoca@hotmail.com"
        message = f"""\
        <h4>New Feedback Submission:</h4>
        <ul>
          <li>Customer: {customer}</li>
          <li>Dealer: {dealer}</li>
          <li>Rating: {rating}</li>
          <li>Comments: {comments}</li>
        </ul>
        """

        msg = MIMEText(message, 'html')
        msg['Subject'] = 'Lexus Feedback'
        msg['From'] = sender
        msg['To'] = receiver

        server.login(user, password)
        server.sendmail(sender, receiver, msg.as_string())
