import cv2
import os
import time

# Tạo thư mục "Data" nếu nó chưa tồn tại
if not os.path.exists("Data"):
    os.makedirs("Data")

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera hoạt động bình thường
if not cap.isOpened():
    print("Không thể mở camera")
    exit()
else : 
    print("Camera đang hoạt động")

# Khởi tạo cửa sổ hiển thị
cv2.namedWindow('Take Picture')



while True:
    # Đếm ngược 3 giây
    for i in range(3, 0, -1): 
        print("Đếm ngược:", i)
        time.sleep(1)

    # Nhập tên của thư mục và tên ảnh
    folder_name = input("Nhập Tên (nhập 'q' để thoát): ")
    ID_number = input("Nhập ID (nhập 'q' để thoát): ")

    # Kiểm tra nếu người dùng muốn thoát
    if (folder_name == 'q') or (ID_number =='q'):
        break

    # Tạo thư mục con trong thư mục "Data" nếu nó chưa tồn tại
    data_folder = "Data/" + folder_name + "_" + ID_number
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Khởi tạo Haar Cascade để phát hiện khuôn mặt
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Chụp 500 ảnh liên tục
    new_size = (231, 231)
    for i in range(5):
        # Đọc ảnh từ camera
        ret, frame = cap.read()

        # Chuyển ảnh sang ảnh mức xám
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Phát hiện khuôn mặt trong ảnh
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)

        # Tạo tên file theo dạng tên và số
        file_name = data_folder + "/" + folder_name + "_" + str(i+1) + ".jpg"

        # Lưu ảnh vào thư mục
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_img_resized = cv2.resize(face_img, new_size)
            cv2.imwrite(file_name, face_img_resized)
        
        # Vẽ hình chữ nhật xung quanh khuôn mặt
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Hiển thị khung hình
        cv2.imshow('frame', frame)

        # Đợi 50ms trước khi chụp ảnh tiếp theo
        cv2.waitKey(50)

        # Chờ 1ms để xử lý sự kiện
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Giải phóng camera
cap.release()

# Đóng cửa sổ
cv2.destroyAllWindows()
