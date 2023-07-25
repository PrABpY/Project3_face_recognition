import face_recognition

known_face_encodings = []
known_face_names = []
person1_location1 = "Prabda"
person1_location2 = "James"

for i in range(0,100):
    person_image = face_recognition.load_image_file("image_train/"+person1_location1+"/face"+str(i)+".jpg")
    if len(face_recognition.face_encodings(person_image)) > 0 :
        print("Read image_train/"+person1_location1+"/face"+str(i)+".jpg")
        known_face_encodings.append(face_recognition.face_encodings(person_image)[0])
        known_face_names.append(person1_location1)