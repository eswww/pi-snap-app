import os
import smtplib
import datetime

from picamera import PiCamera

from pokinator import Pokinator
from PIL import Image, ImageDraw, ImageFont

from email.message import EmailMessage
from email.mime.application import MIMEApplication

def take_picture(camera):
    img_name = Pokinator.generate(generation=2, lowercase=True)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, 'static', img_name)

    camera.capture(img_path)
    camera.stop_preview()

    return img_path

def insert_datetime(image_path):
    img = Image.open(image_path).convert('RGBA')

    ext_size = (img.size[0]+30, img.size[1]+120)
    ext_img = Image.new('RGBA', ext_size, (0, 0, 0, 0))
    ext_img.paste(img, (int((ext_size[0]-img.size[0])/2), 15))

    txt = Image.new('RGBA', ext_img.size, (0, 0, 0, 0))

    fnt = ImageFont.truetype('./static/NanumGothicCoding.ttf', 30)
    tmp = ImageDraw.Draw(txt)

    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tmp.text((15, ext_img.size[1]-65), today, fill='white', font=fnt, align='center')

    img_bin = Image.alpha_composite(ext_img, txt)
    img_bin.save()
    return img_bin

def insert_icon(img_path, light):
    img = Image.open(img_path).convert('RGBA')

    if (light):
        icon = Image.open('./static/sun_icon.png')
    else:
        icon = Image.open('./static/moon_icon.png')
    w_size = int(min(img.size[0], img.size[1]) * 0.25)
    icon_percent = (w_size / float(icon.size[0]))
    h_size = int((float(icon.size[1]) * float(icon_percent)))

    s_image = icon.resize((int(w_size*0.8), int(h_size*0.8)))
    mbox = img.getbbox()
    sbox = s_image.getbbox()

    box = (mbox[2] - sbox[2] - 10, mbox[3] - sbox[3]+30)
    img.paste(s_image, box)

    return img

def send_email(img_path, from_email, to_email):
    img_name = os.path.basename(img_path)

    msg = EmailMessage()
    msg['Subject'] = 'Picture from Pi-Snap!'
    msg['From'] = from_email
    msg['To'] = to_email

    msg.add_alternative(
        '''
        <p>Hello! We are from Pi-Snap!</p>
        <br/>
        <img src="cid:{img_path}" />
        '''.format(img_path=img_name),
        subtype='html'
    )

    with open(img_path, 'rb') as fp:
        img_bin = fp.read()
        
        multi_part = MIMEApplication(img_bin, name=img_name)
        multi_part.add_header('Content-ID', '<' + img_name + '>')
        msg.attach(multi_part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.ehlo()
        smtp.login(from_email, os.environ['GMAIL_PASS'])
        smtp.send_message(msg)


if __name__ == '__main__':
    img = './static/example.jpg'
    send_email(img, 'nojamrobot@gmail.com', 'punkkid001@gmail.com')