from barbearia.email_config import EMAIL_ADDRESS, EMAIL_PASSWORD
import smtplib
from email.message import EmailMessage

def email_cadastro(nome, email):

    msg = EmailMessage()
    msg['Subject'] = 'CADASTRO NA BARBEARIA DOM FIGARO'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f'Olá {nome}, seu cadastro na Barbearia Dom Figaro foi concluído com sucesso.')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email de cadastro de novo usuário enviado com sucesso.")
        except:
            print("O envio do email falhou.")
