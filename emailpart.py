from flask_mail import Mail, Message
from app import app

mail = Mail(app)

def send_email(video_id, email):
    with app.app_context():
        name = 'ADS'
        message = "Your video is dubbed. You can access it from https://ads-f6ms.onrender.com//video/" + video_id + " for any related queries contact us at Automatic.dubbing.software@gmail.com"

        msg = Message('New Message from ' + name, sender='Automatic.dubbing.software@gmail.com',
                      recipients=[email])
        msg.body = message

        mail.send(msg)

