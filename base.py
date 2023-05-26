#Scratch testing

from PIL import Image, ImageDraw, ImageFont, ImageColor

#build black image background
#img = Image.new(mode="RGBA", size=(1080,1350), color='black')
#img.save("background.png")

img = Image.open("background.png")
img2 = Image.open("tensor.png")
img.paste(img2,(100,100))
img.save("test.png")