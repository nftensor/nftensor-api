import bittensor as bt
from PIL import Image, ImageDraw, ImageFont, ImageColor
from textwrap3 import wrap
import nltk

#from user input will need to connect this to UI
input = "What do you know about Pericles?"

#query bittensor with user input
resp = bt.prompt( input, hotkey = "5F4tQyWrhfGVcNhoqeiNsR6KjD4wMZ2kfhLj4oHYuyHbZAc3")

def get_first_sentence(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Return the first sentence
    if sentences:
        return sentences[0]
    else:
        return ""

out = get_first_sentence(resp)

img = Image.open("../assets/imgs/base/background_tao_right.png")
draw = ImageDraw.Draw(img)
width, height = img.size
x = width // 2
y = height // 2
max_font_size = 20

text_color = (255, 255, 255)

font = None
font_size = max_font_size
line_spacing = 1.5

while font_size > 0:
    font = ImageFont.truetype("../assets/fonts/EBGaramond-Regular.ttf", font_size)
    wrapped_text = wrap(out, width=int(width * 1.5 / font_size), break_long_words=False)
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in wrapped_text]
    max_line_height = max(line_heights)
    total_height = sum(line_heights) + int((len(wrapped_text) - 1) * max_line_height * (line_spacing - 1))

    if total_height <= height * 0.8:
        break

    font_size -= 1

if font is None:
    print("Text size OOB")
    # add error handling
    # what should we do here?
else:
    total_height = sum(line_heights) + int((len(wrapped_text) - 1) * max_line_height * (line_spacing - 1))
    y -= total_height // 2

    for line in wrapped_text:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        draw.text((x - line_width // 2, y), line, fill=text_color, font=font)
        y += int(max_line_height * line_spacing)

    img.save("../assets/imgs/out/testout.png")