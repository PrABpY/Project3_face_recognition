import face_recognition
import numpy as np
from statistics import mean 

known_face_encodings = []
known_face_names = []
person1_location = ["BILL","siwakorn","chatchanan"]
d_m = []
n = 0
number_img = 0

for name in person1_location :
    while number_img <= 30:
        person_image = face_recognition.load_image_file("image_train/"+name+"/face"+str(n)+".jpg")
        # print(person_image)
        # print(face_recognition.face_encodings(person_image)[0])
        if len(face_recognition.face_encodings(person_image)) > 0 :
            de = mean(face_recognition.face_encodings(person_image)[0])
            print("Read image_train/"+name+"/face"+str(n)+".jpg",de)
            print(type(face_recognition.face_encodings(person_image)[0]))
            d_m.append(face_recognition.face_encodings(person_image)[0][60])
            known_face_encodings.append(face_recognition.face_encodings(person_image)[0])
            known_face_names.append(name)
            number_img += 1
        n += 1
    # print(d_m)
    # print(mean(d_m))
    d_m = []
    n = 0
    number_img = 0
np.savetxt("data.csv",known_face_encodings,delimiter =",",fmt ='% s')
print(">>>Succesful<<<")
dataset = np.loadtxt("data.csv",delimiter=",", dtype=str)
data = dataset
print(known_face_encodings)
# print(len(known_face_encodings))