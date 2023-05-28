import bittensor as bt
from PIL import Image, ImageDraw, ImageFont, ImageColor
import textwrap

#from user input will need to connect this to UI
input = "Who was Hercules?"

#query bittensor with user input
resp = bt.prompt( input, hotkey = "5F4tQyWrhfGVcNhoqeiNsR6KjD4wMZ2kfhLj4oHYuyHbZAc3")

#take first sentence of resp
per = resp.split(".")
que = resp.split("?")
exc = resp.split("!")

if(len(per[0]) < len(que[0]) and len(per[0]) < len(exc[0])):
    out = per[0] + "."  
elif(len(que[0]) < len(per[0]) and len(que[0]) < len(exc[0])):
    out = que[0] + "?"   
else:
    out = exc[0] + "!"

img = Image.open("background_540x.png")
draw = ImageDraw.Draw(img)
width, height = img.size
x = width // 2
y = height // 2
max_font_size = 20

text_color = (255, 255, 255)  # White text color

font = None
font_size = max_font_size

while font_size > 0:
    font = ImageFont.truetype("/mnt/c/Windows/Fonts/arial.ttf", font_size)
    wrapped_text = textwrap.wrap(out, width=int(width * 0.9 / font_size), break_long_words=False)
    total_height = sum(font.getsize(line)[1] for line in wrapped_text)

    if total_height <= height * 0.8:
        break

    font_size -= 1

if font is None:
    print("Text size OOB")
    # what should we do here?
else:
    total_height = sum(font.getsize(line)[1] for line in wrapped_text)
    y -= total_height // 2

    for line in wrapped_text:
        line_width, line_height = font.getsize(line)
        draw.text((x - line_width // 2, y), line, fill=text_color, font=font)
        y += line_height

    img.save("testout.png")