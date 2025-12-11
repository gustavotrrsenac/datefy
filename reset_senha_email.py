import smtplib
import email.message

def enviar_email():
    corpo_email = """ "<h2>Redefinição de senha</h2>

    <p>Olá,</p>

    <p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>

    <p>Para continuar, utilize o código abaixo:</p>

    <h1 style="font-size: 32px; letter-spacing: 4px; text-align: center;">
        <b>{frhnsgdomanhxnhx}</b>
    </h1>

    <p>Se você não solicitou uma troca de senha, basta ignorar este e-mail. 
    Nenhuma alteração será feita sem sua permissão.</p>

    <p>Atenciosamente,<br>
    Equipe de Suporte</p>"
    """

    msg = email.message.Message()
    msg["Subject"] = "Mensagem titulo"
    msg["From"] = "datefyteste@gmail.com"
    msg["To"] = "datefyteste@gmail.com"
    senha = "frhnsgdomanhxnhx"
    msg.add_header("Content-Type", 'text/html')
    msg.set_payload(corpo_email)

    envia = smtplib.SMTP("smtp.gmail.com: 587")
    envia.starttls()
    envia.login(msg["From"],senha)
    envia.sendmail(msg["From"], [msg["To"]],msg.as_string().encode('utf-8'))
    print("Email enviado!")
enviar_email()