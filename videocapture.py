import face_recognition
import cv2
import numpy as np
import serial

arduino = serial.Serial(port='COM10', baudrate=115200, timeout=.1)
num_train = 40

def check(matches,person1_location):
    num = len(matches)//3
    p1 = matches[0:num].count(True)
    p2 = matches[num:num*2].count(True)
    p3 = matches[num*2:num*3].count(True)
    print(p1,p2,p3)
    if p1 > p2 and p1 > p3 and p1 > num_train//4: return person1_location[0]
    if p2 > p1 and p2 > p3 and p2 > num_train//4: return person1_location[1]
    if p3 > p1 and p3 > p2 and p3 > num_train//4: return person1_location[2]
    return "Unknown"

video_capture = cv2.VideoCapture(1)
# video_capture = cv2.VideoCapture('v.mp4')

dataset = np.loadtxt("data.csv",delimiter=",", dtype=str)
data = []
for i in dataset :
    data.append(np.array(i))
known_face_encodings = []
person1_location = ["Prabda","Jesky","James"]
n = 0
number_img = 0
coun = 0

for name in person1_location :
    while number_img <= num_train:
        person_image = face_recognition.load_image_file("image_train/"+name+"/face"+str(n)+".jpg")
        if len(face_recognition.face_encodings(person_image)) > 0 :
            print("Read image_train/"+name+"/face"+str(n)+".jpg"," True")
            known_face_encodings.append(face_recognition.face_encodings(person_image)[0])
            number_img += 1
        else : print("Read image_train/"+name+"/face"+str(n)+".jpg"," False")
        n += 1
    n = 0
    number_img = 0

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
tec = input("ready : ")
if tec == "yes":
    while True:
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,1)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        if len(face_encodings) > 0 :
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
                per = check(matches,person1_location)
                face_names.append(per)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            font = cv2.FONT_HERSHEY_DUPLEX
            color = (0, 0, 255)
            if name == "Unknown":
                coun = 0
            if name != "Unknown":
                color = (0, 255, 0)
                coun += 1
                if coun == 7 :
                    arduino.write(b'H')
                    # print("W")
            arduino.write(b'L')
            # print(coun)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
video_capture.release()
cv2.destroyAllWindows()

