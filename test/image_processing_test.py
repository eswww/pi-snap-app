# pillow.readthedocs.io/en/5.1.x/reference/ImageDraw.html#example-draw-partial-opacity-text

import datetime
from PIL import Image, ImageDraw, ImageFont

#def insert_datetime(image_path):
img = Image.open('./static/example.jpg').convert('RGBA')

ext_size = (img.size[0]+30, img.size[1]+120)
ext_img = Image.new('RGBA', ext_size, (0, 0, 0, 0))
ext_img.paste(img, (int((ext_size[0]-img.size[0])/2), 15))

txt = Image.new('RGBA', ext_img.size, (0, 0, 0, 0))

fnt = ImageFont.truetype('./static/NanumGothicCoding.ttf', 30)
tmp = ImageDraw.Draw(txt)

today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

tmp.text((15, ext_img.size[1]-65), today, fill='white', font=fnt, align='center')

out = Image.alpha_composite(ext_img, txt)

icon = Image.open('./static/sun_icon.png')
w_size = int(min(out.size[0], out.size[1]) * 0.25)
icon_percent = (w_size / float(icon.size[0]))
h_size = int((float(icon.size[1]) * float(icon_percent)))

s_image = icon.resize((int(w_size*0.8), int(h_size*0.8)))
mbox = out.getbbox()
sbox = s_image.getbbox()

box = (mbox[2] - sbox[2] - 10, mbox[3] - sbox[3]+30)
out.paste(s_image, box)
out.show()