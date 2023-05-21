import matplotlib.pyplot as plt
import os
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model

model1 = load_model('Trained/model_1_face_detection_20146132.h5')

# open webcam
webcam = cv2.VideoCapture(0)

# detectface
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# class 
classes = ['Phong_20146132', 'AnhKiet_20146499', 'Dat_20146488', 'Thach_20146530', 'Thai_20146117']

# loop through frames
while webcam.isOpened():

    # read frame from webcam 
    status, frame = webcam.read()

    #Chuyển ảnh sang mức xám
    grayface = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    #Tách khuôn mặt    
    faces = face_cascade.detectMultiScale(grayface, scaleFactor=1.3, minNeighbors=5)         

    for (x,y,w,h) in faces:
        #Tạo 4 giá trị để tạo hình vuông tập trung vào khuôn mặt
        startX = x
        startY = y
        endX = x + w
        endY = y + h

        #Vẽ hình vuông lên ảnh
        cv2.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)

        #Tạo 1 bản sao cho khuôn mặt vừa được tách
        face_crop = np.copy(frame[startY:endY,startX:endX])

        #Resize bản sao
        #face_crop = np.array(face_crop)
        #face_crop_iden = tf.image.resize(face_crop, [231,231])
        face_crop_iden = cv2.resize(face_crop, [231,231])
        face_crop_iden = np.expand_dims(face_crop_iden, axis=0)
        
        #Máy dự đoán
        iden = model1.predict(face_crop_iden)[0]

        #Tạo biến để nhận kết quả dự đoán của máy
        idx = np.argmax(iden)
        label1 = classes[idx]
        #Tạo chữ hiển thị trên khung ảnh
        label = "{}".format(label1)
        #Vị trí xuất hiện của chữ
        Y = startY - 10 if startY - 10 > 10 else startY + 10

        #Cho hiển thị chữ lên khung ảnh
        cv2.putText(frame, label, (startX, Y),  cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    #Hiển thị hình ảnh đã xử lí
    cv2.imshow("Face_Detection", frame)

    #Nhấn phím "Q" để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Giải phóng dữ liệu
webcam.release()
cv2.destroyAllWindows()