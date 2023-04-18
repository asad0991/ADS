import os
import db_conn
from app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import dubber
import emailpart
from flask import send_file
import threading
@app.route('/')
def upload_form():
    #emailpart.send_email()
    return render_template('upload.html')

@app.route('/upload')
def upload_page():
    #emailpart.send_email()
    return render_template('upload.html')

@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/api/download')
def send_video():
    videoname = request.args.get('videoname')
    #videoname=request.args.get('videoname')
    return send_file('./'+videoname,as_attachment=True)

@app.route('/api/play/<videoname>')
def play(videoname):
    return render_template('play.html',videoname=videoname)

@app.route('/video/<videoid>')
def get_and_play_video(videoid):
    name=db_conn.get_video(videoid)
    return render_template('play.html',videoname=name)


@app.route('/', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
        filename = secure_filename(file.filename)
        original_language = request.form['original']
        Target_language = request.form['target']
        print(filename)
        print(str(original_language))
        print(str(Target_language))
        if original_language == Target_language:
            print("Original language and Target language cannot be same")
        elif filename.endswith('.mp4'):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            background_thread = threading.Thread(target=dubber.dub_video, args=(filename, original_language, Target_language))
            background_thread.start()

           # return send_file("C:/Users/Nadra/PycharmProjects/pythonProject6/dubbed/" + path, as_attachment=True)
            return render_template('uploadsuccess.html')
        else:
            print('File type not supported')
        return render_template('upload.html')


@app.route('/success')
def upload_success():

    return render_template('uploadsuccess.html')


if __name__ == "__main__":
    app.run()

    #db_conn.insert_video()
