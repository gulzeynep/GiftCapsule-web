import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_gift_email(recipient_email: str, gift_data: dict) -> bool:
    """
    Send gift notification email to recipient
    """
    try:
        sender_email = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASSWORD')

        if not sender_email or not password:
            raise ValueError('EMAIL_USER and EMAIL_PASSWORD must be set')

        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = f"🎁 {gift_data['sender_name']} sana bir hediye gönderdi!"
        message['From'] = sender_email
        message['To'] = recipient_email

        # HTML body
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Merhaba {gift_data['recipient_name']}!</h2>
                <p>{gift_data['sender_name']} sana özel bir dijital hediye gönderdi.</p>
                <p>Hediyeni görüntülemek için aşağıdaki linke tıkla:</p>
                <a href="{gift_data['view_link']}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Hediyemi Görüntüle</a>
                <br><br>
                <p>Sevgiyle,<br>GiftCapsule Ekibi</p>
            </body>
        </html>
        """

        part = MIMEText(html, 'html')
        message.attach(part)

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        return True

    except Exception as e:
        print(f'Email sending failed: {str(e)}')
        return False


def send_capsule_email(creator_email: str, capsule_data: dict) -> bool:
    """
    Send time capsule confirmation email
    """
    try:
        sender_email = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASSWORD')

        if not sender_email or not password:
            raise ValueError('EMAIL_USER and EMAIL_PASSWORD must be set')

        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = f"⏰ Zaman Kapsülün Oluşturuldu!"
        message['From'] = sender_email
        message['To'] = creator_email

        # HTML body
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Zaman Kapsülün Başarıyla Oluşturuldu!</h2>
                <p><strong>Başlık:</strong> {capsule_data['title']}</p>
                <p><strong>Açılış Tarihi:</strong> {capsule_data['open_date']}</p>
                <p>Zaman kapsülün belirtilen tarihte açılabilir olacak.</p>
                <p><strong>Capsule açılacağı tarihte bilgilendirme maili gelecektir.</strong></p>
                <p>Zaman kapsülünü görüntülemek için aşağıdaki linke tıkla:</p>
                <a href="{capsule_data['view_link']}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Kapsülümü Görüntüle</a>
                <br><br>
                <p>Sevgiyle,<br>GiftCapsule Ekibi</p>
            </body>
        </html>
        """

        part = MIMEText(html, 'html')
        message.attach(part)

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, creator_email, message.as_string())

        return True

    except Exception as e:
        print(f'Email sending failed: {str(e)}')
        return False


def send_capsule_opened_email(creator_email: str, capsule_data: dict) -> bool:
    """
    Send notification email when capsule opening time arrives
    """
    try:
        sender_email = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASSWORD')

        if not sender_email or not password:
            raise ValueError('EMAIL_USER and EMAIL_PASSWORD must be set')

        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = f"🎉 Zaman Kapsülün Açılma Zamanı Geldi!"
        message['From'] = sender_email
        message['To'] = creator_email

        # HTML body
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>🎉 Müjde! Zaman Kapsülün Açılma Zamanı Geldi!</h2>
                <p><strong>Başlık:</strong> {capsule_data['title']}</p>
                <p>Zaman kapsülün artık açılabilir! Geçmişten geleceğe bir yolculuk seni bekliyor.</p>
                <p>Kapsülünü görüntülemek için aşağıdaki linke tıkla:</p>
                <a href="{capsule_data['view_link']}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Kapsülümü Aç</a>
                <br><br>
                <p>Sevgiyle,<br>GiftCapsule Ekibi</p>
            </body>
        </html>
        """

        part = MIMEText(html, 'html')
        message.attach(part)

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, creator_email, message.as_string())

        return True

    except Exception as e:
        print(f'Email sending failed: {str(e)}')
        return False
