import face_recognition
import cv2

# เปิดการใช้ webcam
video_capture = cv2.VideoCapture(0)

# โหลดภาพ Peen.jpg และให้ระบบจดจำใบหน้า
person1_image = face_recognition.load_image_file("image.jpeg")
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]

# โหลดภาพ Stop.jpg และให้ระบบจดจำใบหน้า
person2_image = face_recognition.load_image_file("image2.jpg")
person2_face_encoding = face_recognition.face_encodings(person2_image)[0]

# สร้าง arrays ของคนที่จดจำและกำหนดชื่อ ตามลำดับ
known_face_encodings = [
    person1_face_encoding,
    person2_face_encoding,
]

known_face_names = [
    "PeePrab",
    "Stop"
]

# ตัวแปรเริ่มต้น
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # ดึงเฟรมภาพมาจากวีดีโอ
    ret, frame = video_capture.read()

    # ย่อขนาดเฟรมเหลือ 1/4 ทำให้ face recognition ทำงานได้เร็วขึ้น
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # แปลงสีภาพจาก BGR (ถูกใช้ใน OpenCV) เป็นสีแบบ RGB (ถูกใช้ใน face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # ประมวลผลเฟรมเว้นเฟรมเพื่อประหยัดเวลา
    if process_this_frame:
        # ค้นหาใบหน้าที่มีทั้งหมดในภาพ จากนั้นทำการ encodings ใบหน้าเพื่อจะนำไปใช้เปรียบเทียบต่อ
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # ทำการเปรียบเทียบใบหน้าที่อยู่ในวีดีโอกับใบหน้าที่รู้จักในระบบ
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # ถ้า encoding แล้วใบหน้าตรงกันก็จะแสดงข้อมูล
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # แสดงผลลัพธ์
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # ขยายเฟรมที่ลดลงเหลือ 1/4 ให้กลับไปอยู่ในขนาดเดิม 
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # วาดกล่องรอบใบหน้า
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # เขียนตัวหนังสือที่แสดงชื่อลงที่กรอบ
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # แสดงรูปภาพผลลัพธ์
    cv2.imshow('Video', frame)

    # กด 'q' เพื่อปิด!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
video_capture.release()
cv2.destroyAllWindows()