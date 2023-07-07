import mysql.connector
import random
import string
import emailpart
from flask import jsonify
import os
def generate_hex_string(length):
    return ''.join(random.choices(string.hexdigits, k=length))

def insert_video(video_path,original_language,target_language, email):
    # connect to the MySQL database
    db = mysql.connector.connect(
        host="35.232.4.90",
        user="root",
        database="video-dubbing",
        password="Asad123@",
    )
    cursor = db.cursor()
    video_id = generate_hex_string(8)
    sql = "SELECT * FROM VIDEO WHERE VIDEO_ID = %s"
    params = (video_id,)
    cursor.execute(sql, params)
    row = cursor.fetchone()
    while row is not None:
        # video id already exists, generate a new one and check again
        video_id = generate_hex_string(8)
        params = (video_id,)
        cursor.execute(sql, params)
        row = cursor.fetchone()
    # read the contents of the video file into a binary variable
    with open(video_path, "rb") as f:
        video_data = f.read()

    filename = video_path.rsplit('/', 1)[-1]
    # prepare the INSERT statement
    sql = "INSERT INTO video (video_id, video, video_title, original_language, target_language, USER_ID) VALUES (%s,%s,%s, %s, %s, %s)"
    params = (video_id, video_data,filename, original_language, target_language, email)

    # create a cursor object and execute the statement

    cursor.execute(sql, params)
    emailpart.send_email(video_id, email)
    # commit the transaction and close the cursor and database connection
    db.commit()
    cursor.close()
    db.close()
    return video_id

def get_video(video_id):
    db = mysql.connector.connect(
        host="35.232.4.90",
        user="root",
        database="video-dubbing",
        password="Asad123@",
    )
    cursor = db.cursor()
    query = "SELECT VIDEO,VIDEO_TITLE FROM video WHERE VIDEO_ID = %s"
    cursor.execute(query, (video_id,))
    data=cursor.fetchone()
    cursor.close()
    db.close()

    file_path = os.path.join("static/dubbed", data[1])
    with open(file_path, 'wb') as f:
        f.write(data[0])

    f.close()
    return data[1]

def user_sign_up(email,name,phone,password, country):
    print("hello")
    db = mysql.connector.connect(
        host="35.232.4.90",
        user="root",
        database="video-dubbing",
        password="Asad123@",
    )
    print("Connection established .... i guess")
    cursor = db.cursor()
    sql = "INSERT INTO users ( NAME,EMAIL, PASSWORD,PHONE_NO, COUNTRY) VALUES (%s,%s,%s, %s, %s)"
    params = (name, email, password, phone, country)

    # create a cursor object and execute the statement

    cursor.execute(sql, params)
    db.commit()
    cursor.close()
    db.close()

def validate_credentials(email,password):
    db = mysql.connector.connect(
        host="35.232.4.90",
        user="root",
        database="video-dubbing",
        password="Asad123@",
    )
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE email = %s AND password = %s"
    params=(email,password)
    cursor.execute(sql, params)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result:
        return True
    else:
        return False

def get_videos_info(email:str):
    db = mysql.connector.connect(
        host="35.232.4.90",
        user="root",
        database="video-dubbing",
        password="Asad123@",
    )
    print(email)
    cursor = db.cursor()
    sql = "SELECT video_id, video_title FROM video WHERE user_id = %s"
    params = (email,)
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    data = []
    for row in result:
        # Assuming the columns are 'id', 'name', and 'email'
        row_dict = {'video_id': row[0], 'video_title': row[1]}
        data.append(row_dict)

    # Return the data as JSON
    return jsonify(data)