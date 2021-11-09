import os
import smtplib
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from config import Config


def send_email():
    sender = Config.EMAIL
    password = Config.PASSWORD

    recipients = ['tagiyevazeandua@gmail.com']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Сообщение
    try:
        with open('blank/email_msg.html', 'r', encoding='utf-8') as email_msg:
            text = email_msg.read().replace('\n', '')
    except IOError as ioe:
        return ioe

    try:
        # Настройка сообщения
        mime_message = MIMEMultipart()

        if text:
            mime_message.attach(MIMEText(text, "html"))

        for attachment in os.listdir('attachments'):
            filename = os.path.basename(attachment)
            filetype, encoding_ = mimetypes.guess_type(attachment)
            filetype, subtype = filetype.split('/')

            if filetype == 'application':
                with open(f'attachments/{filename}', 'rb') as file:
                    data = MIMEApplication(file.read(), subtype)
            else:
                with open(f'attachments/{filename}', 'rb') as file:
                    data = MIMEBase(filetype, subtype)
                    data.set_payload(file.read())
                    encoders.encode_base64(data)

            data.add_header('content-disposition', 'attachment', filename=filename)
            mime_message.attach(data)

        # Отправление сообщения
        for recipient in recipients:
            mime_message['From'] = sender
            mime_message['To'] = recipient
            mime_message['Subject'] = 'Тестовые сообщения.'
            try:
                server.login(sender, password)
                server.sendmail(sender, recipient, mime_message.as_string())
            except Exception as e:
                print(e)
                continue

        return 'Success!'
    except Exception as e:
        print(e)


def main():
    send_email()


if __name__ == '__main__':
    main()
