from http.server import BaseHTTPRequestHandler
import cgi
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Formuliergegevens opvangen
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        # Gegevens uit het formulier halen
        user_email = form.getvalue("from_email")
        recipient = form.getvalue("to_email")
        subject = form.getvalue("subject")
        message_body = form.getvalue("message")
        file_item = form['attachment'] if 'attachment' in form else None

        # 2. Jouw SMTP gegevens (Mailtrap / Mailsandbox)
        smtp_server = "smtp.mailsandbox.com"
        smtp_port = 2525
        smtp_user = "ronaldus.egmond@gmail.com"
        smtp_pass = "lamoraal2025"

        # 3. De e-mail samenstellen
        msg = MIMEMultipart()
        msg['From'] = "hello@example.com" # Jouw 'mail_from_address'
        msg['To'] = recipient
        msg['Subject'] = f"{subject} (via {user_email})"
        
        msg.attach(MIMEText(message_body, 'plain'))

        # Bijlage verwerken
        if file_item is not None and file_item.filename:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_item.file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{file_item.filename}"')
            msg.attach(part)

        # 4. Verzenden
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            # Geen encryptie (mail_encryption=null), dus we gebruiken direct login
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()

            # Na succes sturen we de gebruiker naar een bedankt-pagina
            self.send_response(302)
            self.send_header('Location', '/index.html?status=success')
            self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Fout: {str(e)}".encode())