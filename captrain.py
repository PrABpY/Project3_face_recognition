import cv2
  
video_capture = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
number = 0
while True :
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    print(number)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        faces = frame[y:y + h, x:x + w]
        # cv2.imshow("face",faces)
        cv2.imwrite('image_train/Jesky/face'+str(number)+'.jpg', faces)
        number += 1
          
    # cv2.imwrite('detcted.jpg', img)
    cv2.imshow('img', frame)
    if number >= 100: break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break