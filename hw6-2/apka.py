from flask import Flask
from flask_mail import Message, Mail

app = Flask(__name__)



app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'dgutorka@gmail.com'
app.config['MAIL_PASSWORD'] = 'effe qttb osgr uxen'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)
mail.init_app(app)



@app.route("/email")
def index():
    msg = Message(
        subject="Hello",
        sender="dgutorka@gmail.com",
        recipients=["to@example.com"],
    )

    msg.body = 'Test message'
    mail.send(msg)

    return {'result' : 'success'}
