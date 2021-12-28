import numpy as np
import cv2
import sqlite3


def find_faces(img):
    nparr = np.fromstring(img, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface.xml')
    faces = haar_face_cascade.detectMultiScale(gray_img)
    return len(faces), img_np
    

def create_db():
    conn = sqlite3.connect("saved_media.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS data
                    (id integer PRIMARY KEY AUTOINCREMENT, user_id integer, chat_id integer, type text, path text)
                """)
    conn.commit()


def add_in_db(user_id, chat_id, type, path):
    conn = sqlite3.connect("saved_media.db")
    cursor = conn.cursor()
    d = (user_id, chat_id, type, path)
    cursor.execute("INSERT INTO data(user_id, chat_id, type, path) VALUES(?, ?, ?, ?);", d)
    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect("saved_media.db")
    cursor = conn.cursor()
    cursor.execute("select * from data;")
    all = cursor.fetchall()
    print(all)