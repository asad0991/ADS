import mysql.connector
import random
import string
import emailpart
def generate_hex_string(length):
    return ''.join(random.choices(string.hexdigits, k=length))

def insert_video(video_path,original_language,target_language):
    # connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="video_dubbing",
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
    sql = "INSERT INTO video (video_id, video, video_title, original_language, target_language) VALUES (%s,%s,%s, %s, %s)"
    params = (video_id, video_data,filename, original_language, target_language)

    # create a cursor object and execute the statement

    cursor.execute(sql, params)
    emailpart.send_email(video_id)
    # commit the transaction and close the cursor and database connection
    db.commit()
    cursor.close()
    db.close()
    return video_id

def get_video(video_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="video_dubbing",
    )
    cursor = db.cursor()
    query = "SELECT VIDEO,VIDEO_TITLE FROM VIDEO WHERE VIDEO_ID = %s"
    cursor.execute(query, (video_id,))
    data=cursor.fetchone()
    cursor.close()
    db.close()
    with open(data[1], 'wb') as f:
        f.write(data[0])

    f.close()
    return data[1]