import os

from picamera import PiCamera
from pokinator import Pokinator

from gpiozero import Button
from guizero import App, PushButton, Text, Picture

from image_processing import send_email, insert_datetime, insert_icon


def new_picture():
    global camera, img_path
    camera.start_preview()

def take_picture():
    global camera, img_path

    img_name = Pokinator.generate(generation=2, lowercase=True) + '.png'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, 'static', img_name)

    camera.capture(img_path)
    camera.stop_preview()

    insert_datetime(img_path)
    insert_icon(img_path, True)
    #send_email(img_path, 'nojamrobot@gmail.com', 'punkkid001@gmail.com')


if __name__ == '__main__':
    img_path = 'temporary_path'

    camera = PiCamera()
    camera.resolution = (400, 400)
    camera.hflip = True

    take_pic_btn = Button(25)
    take_pic_btn.when_pressed = take_picture

    camera.start_preview()

    app = App('Pi-Snap')
    txt = Text(app, 'Welcome to Pi-Snap!')
    new_pic_icon = PushButton(app, new_picture, text='New pic')
    app.display()
