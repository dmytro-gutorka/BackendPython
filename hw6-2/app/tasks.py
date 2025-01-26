from flask_mail import Mail, Message
from app import create_app
from celery import Celery

app = create_app()

celery = Celery(app.name, broker=app.config["CELERY"]["broker_url"])
celery.config_from_object(app.config["CELERY"])


@celery.task
def send_async_email(recipient):

    print('message was sent')
    # now it's disabled because it's needed app password for gmail to work


    # from flask import current_app
    #
    # with app.app_context():
    #
    #     mail = Mail(current_app)
    #     mail.init_app(current_app)
    #
    #     msg = Message(
    #         subject="Hello",
    #         sender="dgutorka@gmail.com",
    #         recipients=[recipient],
    #     )
    #
    #     msg.body = 'Your contract has been created'
    #     mail.send(msg)
