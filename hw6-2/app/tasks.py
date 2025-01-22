from flask_mail import Mail, Message
from celery import shared_task


@shared_task
def send_async_email(email_data):
    from flask import current_app

    mail = Mail(current_app)
    msg = Message(
        email_data['subject'],
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email_data['to']],
    )
    msg.body = email_data['body']

    with current_app.app_context():
        mail.send(msg)