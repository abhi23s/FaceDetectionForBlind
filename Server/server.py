import cv2
import numpy as np
import face_recognition as fr
import os
from playsound import playsound
from gtts import gTTS
import random
import threading
from flask import *

print("okkk")
studlist = []
face_flag = 0
chatid = 1102426719
app = Flask(__name__)

known_face_encodings = []
known_face_names = []

def speak(txt):
    mytext = txt
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    val = random.randint(1000, 2000)
    myobj.save("E:\\face_rec\\static\\" + str(val) + ".mp3")
    playsound("E:\\face_rec\\static\\" + str(val) + ".mp3")

def check():
    img_urls = os.listdir('E:\\face_rec\\static\\Pics')
    for i in img_urls:
        imgTest = fr.load_image_file(os.path.join('E:\\face_rec\\static\\Pics', i))
        encodeImgTest = fr.face_encodings(imgTest)[0]
        known_face_encodings.append(encodeImgTest)
        known_face_names.append(i)
    print(known_face_names)

def face_checking():  
    global face_flag
    global studlist
    count = 0

    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while face_flag == 1:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]

        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = fr.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            count += 1
            print(count)

            if count > 15:
                face_flag = 0
                speak("Stranger detected")

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                print(name)
                n = name.replace('.jpg', '')
                face_flag = 0
                speak("The person name " + str(n) + " is in front of you")
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, n, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                cv2.imshow('face_recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()

    return "ok"

def main():
    print("haaaiiii")
    speak("Welcome to the smart blind reader system")
    check()

@app.route('/test', methods=['POST', 'GET'])
def test():
    global face_flag
    b = request.get_data()
    v = b.decode("utf-8")
    print(v)
    if v == "#":
        face_flag = 1
    face_checking()
    return "ok"

if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0', port=5000)
