import os
import threading

from camera import Camera
 
from time import sleep
from multiprocessing import Process
from guizero import App, Box, PushButton, Text, TextBox, Picture


class Application:
    def __init__(self, cam_control):
        # Configuring GUI application
        self.app = App('Pi-Snap', width=1920, height=1200)
        self.cam = Camera()

        self.cam_control = cam_control

        # Main page(frame)
        self.main = Box(self.app)
        self.main_img = Picture(self.main, image='./static/main.png')
        self.new_pic_btn = PushButton(self.main, cam_control, text='New pic')

        # Result page(frame)
        self.result = Box(self.app)
        self.title_txt = Text(self.result, text='Ta-da!', size=40, color='#1956b7')
        self.result_img = Picture(self.result)
        self.guide_txt = Text(
            self.result,
            text='If you want to receive this picture, Please enter your email :)',
            size=25
        )
        self.email_txt = TextBox(self.result, width=25)
        self.send_btn = PushButton(self.result, self.send_email, text='Send')
        self.cancel_btn = PushButton(self.result, self.go_to_main, text='Cancel')
        self.result.visible = False

        self.th = threading.Thread(target=self.read_button)

    def display(self):
        self.th.start()
        self.app.display()

    def read_button(self):
        button = os.open('/dev/button_driver', os.O_RDWR)
        while True:
            if not os.read(button, 0):
                self.cam_control()
                sleep(2)
        os.close(button)

    def go_to_result(self, img_path, email_addr=None):
        self.main.visible = False
        self.result.visible = True
        self.result_img.image = img_path

    def go_to_main(self):
        self.result.visible = False
        self.main.visible = True

    def set_result_image(self, img_path):
        self.result_img.image = img_path

    def new_picture(self):
        self.cam.new_picture()

    def take_picture(self):
        return self.cam.take_picture()

    def send_email(self):
        email_addr = self.email_txt.value
        proc = Process(target=self.cam.send_email, args=(email_addr,))
        proc.start()
        self.email_txt.value = ''

        return self.go_to_main()
