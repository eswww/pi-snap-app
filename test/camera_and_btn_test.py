from guizero import App, PushButton, Text, Picture
from gpiozero import Button
from picamera import PiCamera
from time import gmtime, strftime

def take_picture():
    print('take a picture')
    camera.capture(output)
    camera.stop_preview()

def new_picture():
    camera.start_preview()

new_pic_btn = Button(13)
new_pic_btn.when_pressed = new_picture
take_pic_btn = Button(25)
take_pic_btn.when_pressed = take_picture

camera = PiCamera()
camera.resolution = (400, 400)
camera.hflip = True
camera.start_preview()

output = strftime('./image-%d-%m %H:%M.png', gmtime())

app = App('hello world', 400, 400)
msg = Text(app, 'I spotted u!')
new_pic = PushButton(app, new_picture, text='new pic')
app.display()
