#---------------------------------------------------------------------------------------------------------------#
#                                                   (THƯ VIỆN)                                                  #
#---------------------------------------------------------------------------------------------------------------#
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import face_recognition

#---------------------------------------------------------------------------------------------------------------#
#                                        (KHỞI TẠO CỬA SỔ GIAO DIỆN)                                            #
#---------------------------------------------------------------------------------------------------------------#

# Tạo cửa sổ chính của ứng dụng GUI
win = Tk()
#Thêm tiêu đề cho cửa sổ
win.title('Face Detection System')
#Đặt kích thước của cửa sổ
win.geometry('900x640+300+50')
# Cố định kích thước cửa sổ
win.resizable(False, False)

#---------------------------------------------------------------------------------------------------------------#
#                                          (KHAI BÁO BIẾN, ĐƯỜNG DẪN)                                           #
#---------------------------------------------------------------------------------------------------------------#

# Khai báo biến toàn cục để theo dõi trạng thái camera
video_capture = None
# Biến toàn cục để theo dõi trạng thái của việc hiển thị khung chữ nhật
show_rectangle = False

#---------------------------------------------------------------------------------------------------------------#
#                                         (TẠO HÀM XỬ LÝ CHỨC NĂNG)                                             #
#---------------------------------------------------------------------------------------------------------------#

# Hàm để bật camera và cập nhật hình ảnh lên background
def turn_on_camera():
    global video_capture, show_rectangle
    video_capture = cv2.VideoCapture(0)  # Số 0 đại diện cho camera mặc định
    
    # Hàm cập nhật hình ảnh lên background_label
    def update_frame():
        ret, frame = video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi sang định dạng RGB
            frame = cv2.resize(frame, (400, 300))  # Điều chỉnh kích thước hình ảnh
            
            # Hiển thị khung chữ nhật nếu biến show_rectangle là True
            if show_rectangle:
                face_locations = face_recognition.face_locations(frame)
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Hiển thị hình ảnh lên background_label
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)
            background_label.configure(image=photo)
            background_label.image = photo
        
        if video_capture.isOpened():
            # Gọi lại hàm sau 10ms để cập nhật frame tiếp theo
            win.after(10, update_frame)
        else:
            # Camera đã bị tắt, cập nhật background với ảnh mặc định
            background_label.configure(image=background_photo)
            background_label.image = background_photo
    
    update_frame()

# Hàm để tắt camera
def turn_off_camera():
    global video_capture, show_rectangle
    if video_capture is not None:
        video_capture.release()
    video_capture = None
    show_rectangle = False
    # Cập nhật background với ảnh mặc định
    background_label.configure(image=background_photo)
    background_label.image = background_photo
    btn_START.configure(state="normal")  # Kích hoạt nút START

# Xử lý sự kiện khi nhấn nút ON
def on_button_on_click():
    btn_ON.configure(state="disabled")  # Vô hiệu hóa nút ON
    btn_OFF.configure(state="normal")  # Kích hoạt nút OFF
    turn_on_camera()

# Xử lý sự kiện khi nhấn nút OFF
def on_button_off_click():
    btn_OFF.configure(state="disabled")  # Vô hiệu hóa nút OFF
    btn_ON.configure(state="normal")  # Kích hoạt nút ON
    turn_off_camera()

# Xử lý sự kiện khi nhấn nút START
def on_button_start_click():
    global show_rectangle
    show_rectangle = True
    btn_START.configure(state="disabled")  # Vô hiệu hóa nút START
    btn_STOP.configure(state="normal")  # Kích hoạt nút STOP
    turn_on_camera()

# Xử lý sự kiện khi nhấn nút STOP
def on_button_stop_click():
    btn_STOP.configure(state="disabled")  # Vô hiệu hóa nút STOP
    btn_START.configure(state="normal")  # Kích hoạt nút START
    turn_off_camera()


# Hàm để thoát khỏi chương trình giao diện
def quit_program():
    if video_capture is not None:
        turn_off_camera()  # Tắt camera trước khi thoát
    win.quit()
# Xử lý sự kiện khi nhấn nút QUIT
def on_button_quit_click():
    quit_program()
# Xử lý sự kiện bàn phím
def on_key_press(event):
    if event.char.lower() == "q":
        quit_program()



#---------------------------------------------------------------------------------------------------------------#
#                                               (TẠO GIAO DIỆN)                                                 #
#---------------------------------------------------------------------------------------------------------------#

# Khung nổi đề tài
frame_topic = tk.Frame(win, borderwidth=4, relief="solid")
frame_topic.place(x=50, y=10, width=800, height=60)
lbl_topic = tk.Label(frame_topic, text="FACE DETECTION SYSTEM", font=("Times New Roman", 25,"bold"))
lbl_topic.place(x=170, y=5)

# Khung nổi "Camera"
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(win, image=background_photo)
background_label.place(x=20, y=120, width=400, height=300)
lbl_camera = tk.Label(win, text="CAMERA", fg="red", font=("Times New Roman", 16,"bold"))
lbl_camera.place(x=170, y=80)

# Khung nổi "AUTHOR"
frame_image = Image.open("Author_DangThanhPhong.jpg")
frame_photo = ImageTk.PhotoImage(frame_image)
frame_label = Label(win, image=frame_photo)
frame_label.place(x=550, y=120, width=231, height=231)
lbl_image = tk.Label(win, text="AUTHOR", fg="red", font=("Times New Roman", 16,"bold"))
lbl_image.place(x=620, y=80)

# Tạo nút nhấn "ON", "OFF"
btn_ON = tk.Button(win, text="ON", fg="blue", font=("Times New Roman", 16,"bold"), borderwidth=2, relief="solid", command=on_button_on_click)
btn_ON.place(x=20, y=450, width=60, height=30)
btn_OFF = tk.Button(win, text="OFF", fg="red", font=("Times New Roman", 16,"bold"), borderwidth=2, relief="solid", command=on_button_off_click)
btn_OFF.place(x=360, y=450, width=60, height=30)

# Tạo nút nhấn "START", "STOP", "QUIT"
frame_option = tk.Frame(win, bg="green", borderwidth=2, relief="solid")
frame_option.place(x=20, y=500, width=400, height=60)
btn_START = tk.Button(win, text="START", fg="blue", font=("Times New Roman", 16,"bold"), borderwidth=2, relief="solid", command=on_button_start_click)
btn_START.place(x=40, y=510, width=80, height=40)
btn_STOP = tk.Button(win, text="STOP", fg="red", font=("Times New Roman", 16,"bold"), borderwidth=2, relief="solid", command=on_button_stop_click)
btn_STOP.place(x=180, y=510, width=80, height=40)
btn_QUIT = tk.Button(win, text="QUIT", font=("Times New Roman", 16,"bold"), borderwidth=2, relief="solid", command=on_button_quit_click)
btn_QUIT.place(x=320, y=510, width=80, height=40)

# Khung nổi họ và tên
frame_name = tk.Frame(win, borderwidth=3, relief="solid")
frame_name.pack(side="bottom", pady=10)
lbl_name = tk.Label(frame_name, text="DANG THANH PHONG - 20146132", font=("Times New Roman", 20, "bold"))
lbl_name.pack()

# Tạo textbox dùng để hiển thị thông tin sau khi nhận dạng
textbox_show_inf = tk.Text(win, borderwidth=1, relief="solid")
textbox_show_inf.place(x=550, y=420, width=231, height=50)
lbl_show_inf = tk.Label(win, text="INFO : Name and ID", fg="red", font=("Times New Roman", 16,"bold"))
lbl_show_inf.place(x=570, y=380)




#---------------------------------------------------------------------------------------------------------------#
#                                              (XỬ LÝ CHỨC NĂNG PHỤ)                                            #
#---------------------------------------------------------------------------------------------------------------#

# Gán sự kiện bàn phím
win.bind("<KeyPress>", on_key_press)

# Gọi vòng lặp sự kiện chính để các hành động có thể diễn ra trên màn hình máy tính của người dùng
win.mainloop()