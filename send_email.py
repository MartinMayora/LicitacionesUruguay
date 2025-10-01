import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime

load_dotenv()

def create_email_body_from_csv(csv_path, fecha=None):
    try:
        df = pd.read_csv(csv_path)
        
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        email_body = f"Licitaciones interesantes para la fecha: {fecha}\n\n"
        email_body += "Se han encontrado las siguientes licitaciones:\n\n"
        
        for idx, row in df.iterrows():
            email_body += f"{idx + 1}. Licitación ID: {row['id']}\n"
            email_body += f"   Enlace: {row['link']}\n\n"
        
        email_body += f"\nTotal de licitaciones encontradas: {len(df)}\n"
        return email_body
        
    except Exception as e:
        return f"Error al procesar el archivo CSV: {e}"

def create_html_email_body_from_csv(csv_path, fecha=None):
    try:
        df = pd.read_csv(csv_path)
        
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        html_body = f"""
        <html>
        <body>
            <h2>Licitaciones interesantes para la fecha: {fecha}</h2>
            <p>Se han encontrado las siguientes licitaciones:</p>
        """
        
        for idx, row in df.iterrows():
            html_body += f"""
            <div style="margin: 10px 0; padding: 8px; background: #f0f0f0;">
                <strong>{idx + 1}. Licitación ID: {row['id']}</strong><br>
                <a href="{row['link']}">{row['link']}</a>
            </div>
            """
        
        html_body += f"""
            <p><strong>Total de licitaciones encontradas: {len(df)}</strong></p>
        </body>
        </html>
        """
        return html_body
        
    except Exception as e:
        return f"<p>Error al procesar el archivo CSV: {e}</p>"

def send_email_with_csv(csv_path, receiver_email, fecha=None, use_html=True):
    sender_email = os.getenv('USER_GMAIL')
    sender_password = os.getenv('PASSWORD_GMAIL')
    
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    
    if use_html:
        message_body = create_html_email_body_from_csv(csv_path, fecha)
    else:
        message_body = create_email_body_from_csv(csv_path, fecha)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Licitaciones del día - {fecha}"
    
    if use_html:
        msg.attach(MIMEText(message_body, 'html'))
    else:
        msg.attach(MIMEText(message_body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(sender_email, sender_password)  
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_email_with_csv(
        csv_path="licitacionesInteresantes.csv",
        receiver_email="martinmayora@gmail.com",
        fecha="2024-01-15",
        use_html=False
    )
    