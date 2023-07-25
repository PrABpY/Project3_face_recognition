import face_recognition
import cv2

def check(matches,person1_location):
    num = len(matches)//3
    p1 = matches[0:num].count(True)
    p2 = matches[num:num*2].count(True)
    p3 = matches[num*2:num*3].count(True)
    if p1 > p2 and p1 > p3 : return person1_location[0]
    if p2 > p1 and p2 > p3 : return person1_location[1]
    if p3 > p1 and p3 > p2 : return person1_location[2]
    return "Unknown"

video_capture = cv2.VideoCapture(1)
# video_capture = cv2.VideoCapture('v.mp4')

known_face_encodings = []
known_face_names = []
person1_location = ["ray","Prabda","BILL"]
n = 0
number_img = 0

for name in person1_location :
    while number_img <= 30:
        person_image = face_recognition.load_image_file("image_train/"+name+"/face"+str(n)+".jpg")
        # print(person_image)
        # print(face_recognition.face_encodings(person_image)[0])
        if len(face_recognition.face_encodings(person_image)) > 0 :
            print("Read image_train/"+name+"/face"+str(n)+".jpg",len(face_recognition.face_encodings(person_image)[0]))
            known_face_encodings.append(face_recognition.face_encodings(person_image)[0])
            known_face_names.append(name)
            number_img += 1
        n += 1
    n = 0
    number_img = 0

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

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
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            per = check(matches,person1_location)
            # print(per)
            face_names.append(per)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        font = cv2.FONT_HERSHEY_DUPLEX
        if name == "Unknown":
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else :
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            ####-----------------------------------------



            ####-----------------------------------------
    
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
video_capture.release()
cv2.destroyAllWindows()