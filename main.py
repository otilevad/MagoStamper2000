from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

img = Image.open(filedialog.askopenfilename())

destino = filedialog.askdirectory()
image_name = img.filename.split('/')[-1].split('.')
nome = f'{image_name[0]}-MagoStamper3000.{image_name[1]}'

img = ImageOps.exif_transpose(img)

width, height = img.size

bigger_side = max(width, height)

font_size = (bigger_side/35.45)
font_stroke = (font_size/21.66)
margin = (bigger_side/13.55)

exif_data = img.getexif()
 
date_time = exif_data.get(306, "Unknown")
print(f"Date and Time: {date_time}")

font= ImageFont.truetype('fonts/Comic Sans MS.ttf', font_size)
draw = ImageDraw.Draw(img)

text = "magodavos esteve aqui..."

try:
    date_time_array = date_time.split()
    date_array = date_time_array[0].split(':')
    time_array = date_time_array[1].split(':')
    print(date_array[0])
    text = (f"{date_array[2]}/{date_array[1]}/{date_array[0]} {time_array[0]}:{time_array[1]}")
except:
    text = "magodavos esteve aqui..."

bbox = draw.textbbox((0, 0), text=text, font=font)
textwidth = bbox[2] - bbox[0]
textheight = bbox[3] - bbox[1]

x = width - textwidth - margin
y = height - textheight - margin

draw.text((x, y), text, font = font, fill=(253, 162, 0), stroke_width=font_stroke, stroke_fill=(0, 0, 0))
#img.show()

path_inteiro = f'{destino}/{nome}'

img.save(path_inteiro)