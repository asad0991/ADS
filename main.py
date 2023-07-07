import os
import db_conn
from app import app
from flask import flash, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
import dubber
from flask import send_file
import threading
adsapp=app
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        # Validate the user's credentials against the database or any authentication system
        if db_conn.validate_credentials(email, password):
            # Successful sign-in, set the session as permanent (persistent) and store the sign-in status
            session.permanent = True
            session['logged_in'] = True

            # Redirect to a different page
            return redirect('/dashboard')
        else:
            # Invalid credentials, display an error message
            error_message = "Invalid email or password"
            return render_template('signin.html', error=error_message)

    # GET request, display the sign-in form
    return render_template('signin.html')


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        # User is logged in
        return render_template('dashboard.html')
    else:
        # User is not logged in, redirect to the sign-in page
        return redirect('/signin')


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session.clear()  # Clear the session data
    return redirect(url_for('signin'))














@app.route('/upload')
def upload_form():
    if session.get('logged_in'):
        #emailpart.send_email()
        if session['alert_message'] != "":
            mes=session['alert_message']
            session['alert_message'] = ""
            return render_template('upload.html', message=mes)
        else:
            return render_template('upload.html')
    else:
        return render_template('signin.html')


@app.route('/')
def index():
    session['alert_message'] = ""
    return render_template('signin.html')



@app.route('/api/download')
def send_video():
    if not session.get('logged_in'):
        # User is logged in
        return render_template('signin.html')
    else:
        videoname = request.args.get('videoname')
        #videoname=request.args.get('videoname')
        return send_file('static\\dubbed\\'+videoname,as_attachment=True)

@app.route('/api/play/<videoname>')
def play(videoname):
    if session.get('logged_in'):
        return render_template('play.html',videoname=videoname)
    else:
        return render_template('signin.html')

@app.route('/video/<videoid>')
def get_and_play_video(videoid):
    if not session.get('logged_in'):
        # User is logged in
        return render_template('signin.html')
    else:
        name=db_conn.get_video(videoid)
        return render_template('play.html',videoname=name)


@app.route('/upload_video', methods=['POST'])
def upload_video():
    print("Hello world")
    session['alert_message'] = ""
    if not session.get('logged_in'):
        # User is logged in
        return render_template('signin.html')
    else:
        file=''
        filename=''
        if 'link' in request.form:
            link = request.form['link']
            filename = link.split('/')[-1]

            if 0:
                flash('Invalid link')
                return redirect(request.url)
            else:
                original_language = request.form['original']
                Target_language = request.form['target']
                if original_language.split("-")[0] == Target_language.split("-")[0]:
                    print("Original language and Target language cannot be same")
                    session['alert_message'] = "Original language and Target language cannot be same"

                    return redirect('/upload')
                filename=dubber.download_video(link)
                print("Hello world")

        else:
            file = request.files['file']
            filename = secure_filename(file.filename)





        original_language = request.form['original']
        Target_language = request.form['target']
        print(filename)
        print(str(original_language))
        print(str(Target_language))
        if original_language.split("-")[0] == Target_language.split("-")[0]:
            print("Original language and Target language cannot be same")
            session['alert_message']="Original language and Target language cannot be same"

            return redirect('/upload')
        elif filename.endswith('.mp4'):
            if 'link' not in request.form:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            background_thread = threading.Thread(target=dubber.dub_video,
                                                 args=(filename, original_language, Target_language,session['email'] ))
            background_thread.start()

            return render_template('uploadsuccess.html')
        else:
            print('File type not supported')
            session['alert_message'] = "File Type Not Supported"
            return redirect('/upload')




@app.route('/signup', methods=['POST'])
def signup():
    print("Hello")
    email = request.form['email']
    name = request.form['name']
    country = request.form['country']
    phone = request.form['phone']
    password = request.form['password']

    db_conn.user_sign_up(email, name, phone, password, country)
    return 'Form submitted successfully'

@app.route('/getvideosinfo', methods=['GET', 'POST'])
def get_videos_info():
    data = db_conn.get_videos_info(session.get('email'))
    print(data)
    return data
