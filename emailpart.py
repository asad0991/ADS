from flask_mail import Mail, Message
from app import app

mail = Mail(app)

def send_email(video_id):
    with app.app_context():
        name = 'ADS'
        # email = 'Automatic.Dubbing.Software@gmail.com'
        message = "Your video is dubbed. You can access it from 127.0.0.1:5000/video/" + video_id + " for any related queries contact us at Automatic.dubbing.software@gmail.com"

        msg = Message('New Message from ' + name, sender='Automatic.dubbing.software@gmail.com',
                      recipients=['au62805@gmail.com'])
        msg.body = message

        mail.send(msg)

