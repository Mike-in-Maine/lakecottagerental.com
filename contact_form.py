# This contact form is UNTESTED and needs to be set up completely from scratch
# 12/16/2024

import http.server
import socketserver
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = 8000

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("contact_form.html", "r") as file:
                self.wfile.write(file.read().encode())

    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse the form data
            form_data = urllib.parse.parse_qs(post_data.decode())
            name = form_data.get("name", [""])[0]
            email = form_data.get("email", [""])[0]
            message = form_data.get("message", [""])[0]

            # Send email
            self.send_email(name, email, message)

            # Respond with a success message
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Thank you for contacting us! Your message has been sent.")

    def send_email(self, name, email, message):
        # Email credentials
        sender_email = "youremail@example.com"
        receiver_email = "receiver@example.com"
        password = "yourpassword"  # Make sure to use an app-specific password if needed

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"New Contact Message from {name}"

        body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # Send the email using SMTP
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")

# Run the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
