from http.server import BaseHTTPRequestHandler
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Lees de lengte van de data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # 2. Parse de data (zet het om naar een leesbaar woordenboek)
            fields = urllib.parse.parse_qs(post_data)

            # Velden ophalen (met fallback waarde)
            user_email = fields.get('from_email', [''])[0]
            recipient  = fields.get('to_email', [''])[0]
            subject    = fields.get('subject', ['Geen onderwerp'])[0]
            message    = fields.get('message', [''])[0]

            # 3. SMTP instellingen (Mailtrap / Mailsandbox)
            smtp_server = "smtp.mailsandbox.com"
            smtp_port   = 2525
            smtp_user   = "ronaldus.egmond@gmail.com" # Jouw username
            smtp_pass   = "lamoraal2025"   # Jouw password
            mail_from_address = "hello@example.com"

            # 4. Mail opstellen
            msg = MIMEMultipart()
            msg['From'] = mail_from_address
            msg['To'] = recipient
            msg['Subject'] = f"{subject} (van: {user_email})"
            msg.attach(MIMEText(message, 'plain'))

            # 5. Verzenden
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()

            # Succes! Stuur terug naar de site
            self.send_response(302)
            self.send_header('Location', '/index.html?mail=verzonden')
            self.end_headers()

        except Exception as e:
            # Foutafhandeling: laat de fout zien in de browser voor nu
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            error_message = f"Fout in script: {str(e)}"
            self.wfile.write(error_message.encode())