from http.server import BaseHTTPRequestHandler
import cgi
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Formuliergegevens uitlezen
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        email_from = form.getvalue("from")
        email_to = form.getvalue("to")
        subject = form.getvalue("subject")
        message_body = form.getvalue("message")
        file_item = form['attachment'] if 'attachment' in form else None

        # 2. SMTP Instellingen (Vul hier je eigen gegevens in)
        smtp_server = "smtp.jouwprovider.nl"
        smtp_port = 587
        smtp_user = "jouw@email.nl"
        smtp_pass = "jouw-wachtwoord"

        # 3. Email opstellen
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(message_body, 'plain'))

        # Bijlage verwerken
        if file_item is not None and file_item.filename:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_item.file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_item.filename}')
            msg.attach(part)

        # 4. Verzenden via SMTP
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()

            self.send_response(302)
            self.send_header('Location', '/bedankt.html') # Stuur door naar bedankt pagina
            self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Fout bij verzenden: {str(e)}".encode())