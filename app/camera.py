import os

from PIL import Image
from time import sleep

from picamera import PiCamera
from pokinator import Pokinator

from image_processing import send_email, insert_datetime, insert_icon


class Camera:
    def __init__(self):
        self.cam = PiCamera()
        self.cam.resolution = (400, 400)
        self.cam.hflip = True
        self.cam.led = False

        self.img = None

    def is_preview(self):
        return self.cam.preview

    def set_brightness(self, light):
        if light:
            self.cam.brightness = 50
            self.cam.contrast = 50
        else:
            self.cam.brightness = 70
            self.cam.contrast = 10

    def new_picture(self):
        self.cam.led = True
        self.cam.start_preview()

    def take_picture(self):
        # Configure directory path and image file name
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        img_name = Pokinator.generate(
            generation=2, lowercase=True
        ) + '.png'

        img_path = os.path.join(
            base_dir, 'saved_images', img_name
        )

        # Add overlay (countdown)
        img_list = (
            './static/overlay_img_3.png',
            './static/overlay_img_2.png',
            './static/overlay_img_1.png'
        )
        overlay_img_list = list()

        for img in img_list:
            overlay_img_list.append(Image.open(img))

        for overlay_img in overlay_img_list:
            pad = Image.new('RGBA', (
                ((overlay_img.size[0] + 31) // 32) * 32,
                ((overlay_img.size[1] + 15) // 16) * 16,
            ))
            pad.paste(overlay_img, (0, 0))
            overlay = self.cam.add_overlay(
                pad.tobytes(),
                size=overlay_img.size,
                layer=3,
                alpha=100
            )
            sleep(1)
            self.cam.remove_overlay(overlay)

        # Capture the image
        self.cam.capture(img_path)
        self.cam.stop_preview()
        self.cam.led = False

        # Save image file path
        self.img = img_path

        # Insert icon and datetime
        insert_datetime(img_path)
        insert_icon(img_path, True)

        return self.img

    def final_process(self, email_addr):
        # Send an email or back to main
        send_email(self.img, 'nojamrobot@gmail.com', email_addr)
        self.img = None
