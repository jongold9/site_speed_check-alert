import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_response_time(url):
    try:
        response = requests.get(url)
        return response.elapsed.total_seconds()
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        return None

def send_email(sender_email, password, receiver_email, subject, message):
    try:
        # Create the MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Add the body of the message
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        # Add the date and time
        msg['Date'] = time.strftime('%d %b %Y %H:%M:%S')

        # Connect to the server and send the message
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

def main():
    urls = []
    with open("urls.txt", "r") as f:
        for line in f:
            urls.append(line.strip())

    # Sender and recipient email addresses
    sender_email = "my1@gmail.com"
    password = "my_pass"
    receiver_email = "my2@gmail.com"

    previous_response_times = {}

    while True:
        for url in urls:
            current_response_time = get_response_time(url)
            if current_response_time and current_response_time > 4:
                print(f"Response time for {url} increased to {current_response_time} seconds.")
                send_email(sender_email, password, receiver_email, "Response time alert", f"Response time for {url} is {current_response_time} seconds.\n\nTested on {time.strftime('%d %b %Y %H:%M:%S')}.")

            previous_response_times[url] = current_response_time

        time.sleep(320)

if __name__ == "__main__":
    main()

