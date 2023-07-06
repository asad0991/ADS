from flask import Flask
from datetime import timedelta
UPLOAD_FOLDER = 'static/uploads/'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'automatic.dubbing.software@gmail.com'
app.config['MAIL_PASSWORD'] = 'lhtoyomijxunfwve'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

