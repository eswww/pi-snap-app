import os
import smtplib
import datetime

from PIL import Image, ImageDraw, ImageFont

from email.message import EmailMessage
from email.mime.application import MIMEApplication


def insert_datetime(img_path):
    # Open image
    img = Image.open(img_path).convert('RGBA')

    # Add a border
    border_size = (img.size[0] + 30, img.size[1] + 120)
    border_img = Image.new('RGBA', border_size, (255, 255, 255, 255))
    border_img.paste(img, (int((border_size[0] - img.size[0]) / 2), 15))

    # Add a text (datetime)
    txt = Image.new('RGBA', border_img.size, (0, 0, 0, 0))
    fnt = ImageFont.truetype('./static/NanumGothicCoding.ttf', 30)
    fnt_point = (15, border_img.size[1] - 65)

    tmp = ImageDraw.Draw(txt)
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tmp.text(
        fnt_point,
        today,
        fill='black',
        font=fnt,
        align='center'
    )

    # Save image
    img = Image.alpha_composite(border_img, txt)
    img.save(img_path)
    img.close()

def insert_icon(img_path, light):
    # Open image
    img = Image.open(img_path).convert('RGBA')

    # Day sun / Night moon
    if light:
        icon = Image.open('./static/sun_icon.png')
    else:
        icon = Image.open('./static/moon_icon.png')

    # Find point
    point = (
        img.size[0] - icon.size[0] - 15,
        img.size[1] - icon.size[1] - 7
    )

    # Save image
    img.paste(icon, point)
    img.save(img_path)
    img.close()

def send_email(img_path, from_email, to_email):
    img_name = os.path.basename(img_path)

    # Email message object
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

    # Add an image to email
    with open(img_path, 'rb') as fp:
        img_bin = fp.read()
        
        multipart = MIMEApplication(img_bin, name=img_name)
        multipart.add_header('Content-ID', '<' + img_name + '>')
        msg.attach(multipart)

    # Send an email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.ehlo()
        smtp.login(from_email, os.environ['GMAIL_PASS'])
        smtp.send_message(msg)
