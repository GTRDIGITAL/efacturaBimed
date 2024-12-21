import ssl
import datetime
import base64
import smtplib
from flask import session
from .sendMails import *

def trimitereOTPMail(code, destinatari):
    smtp_server = "smtp.office365.com"
    port = 587  # Pentru starttls
    sender_email = "GTRDigital@ro.gt.com"
    password = "g[&vuBR9WQqr=7>D"
    context = ssl.create_default_context()
    message_text = f"Buna ziua,\n\nCodul de autentificare este {code}\n\nThank you,\nGTRDigital"
    
    data = datetime.datetime.now()

    # Adăugați 2 ore
    data_modificata = data + datetime.timedelta(hours=2)

    # Formatați data modificată după nevoie
    data_modificata_formatata = data_modificata.strftime("%d/%m/%Y %H:%M")
    subj = "Cod OTP eFactura" 
    mailTo = destinatari
    atasament=""
    cc_recipients=""
    send_email_via_graph_api(subj, destinatari,message_text ,atasament,cc_recipients)