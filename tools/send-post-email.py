#!/usr/bin/env python3
import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

def send_post_email(recipient_email, subject, html_file):
    EMAIL_USER = os.getenv("EMAIL_USER", "polakenfold@gmail.com")
    EMAIL_PASS = os.getenv("EMAIL_PASS", "ghca olpq vdav pllw")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"Email enviado a {recipient_email}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Uso: python3 send-post-email.py <email_destino> <asunto> <archivo_html>")
        sys.exit(1)
    
    send_post_email(sys.argv[1], sys.argv[2], sys.argv[3])