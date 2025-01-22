from flask_mail import Mail, Message
from app import create_app
from celery import Celery

app = create_app()

celery = Celery(app.name, broker=app.config["CELERY"]["broker_url"])
celery.config_from_object(app.config["CELERY"])

@celery.task
def send_async_email():
    from flask import current_app

    with app.app_context():

        mail = Mail(current_app)
        mail.init_app(current_app)

        msg = Message(
            subject="Hello",
            sender="dgutorka@gmail.com",
            recipients=["to@example.com"],
        )

        msg.body = 'Test message'
        mail.send(msg)
