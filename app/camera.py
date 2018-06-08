import os

from picamera import PiCamera
from pokinator import Pokinator

from image_processing import send_email, insert_datetime, insert_icon


class Camera:
    def __init__(self):
        self.cam = PiCamera()
        self.cam.resolution = (400, 400)
        self.cam.hflip = True

        self.img = None

    def new_picture(self):
        self.cam.start_preview()

    def take_picture(self):
        img_name = Pokinator.generate(generation=2, lowercase=True) + '.png'
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, 'static', img_name)

        self.cam.capture(img_path)
        self.cam.stop_preview()

        self.img = img_path

        insert_datetime(img_path)
        insert_icon(img_path, True)

    def final_process(self, email_addr, is_send):
        if is_send:
            send_email(self.img, 'nojamrobot@gmail.com', email_addr)
        else:
            self.img = None
