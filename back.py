## python será apenas usado para mandar emails de forma automática.

import imaplib
import email
from email.header import decode_header

# Informações de conexão (substitua com suas credenciais)
imap_server = "seu_servidor_imap.com"  # Ex: imap.gmail.com, outlook.office365.com
email_address = "seu_email@exemplo.com"
password = "sua_senha"

def receber_emails_imap():
    try:
        # Conectar ao servidor IMAP
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)

        # Selecionar a caixa de correio (ex: INBOX)
        mail.select("INBOX")

        # Pesquisar por e-mails (ex: todos os e-mails NÃO lidos)
        status, email_ids = mail.search(None, "UNSEEN")
        if status == "OK":
            for email_id in email_ids[0].split():
                # Obter o e-mail
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status == "OK":
                    msg = email.message_from_bytes(msg_data[0][1])
                    assunto = ""
                    remetente = ""

                    # Decodificar o assunto (pode conter caracteres especiais)
                    for part, encoding in decode_header(msg["Subject"]):
                        if isinstance(part, bytes):
                            assunto += part.decode(encoding or "utf-8")
                        else:
                            assunto += part

                    # Decodificar o remetente
                    for part, encoding in decode_header(msg.get("From")):
                        if isinstance(part, bytes):
                            remetente += part.decode(encoding or "utf-8")
                        else:
                            remetente += part

                    print(f"Assunto: {assunto}")
                    print(f"Remetente: {remetente}")
                    print("-" * 30)

                    # Marcar o e-mail como lido (opcional)
                    # mail.store(email_id, "+FLAGS", "\\Seen")

        # Desconectar do servidor
        mail.logout()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    receber_emails_imap()