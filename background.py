from PIL import Image

# Create a new grayscale square image
image = Image.new("L", (540, 540), "black")

# Save the image
image.save("black_square_grayscale.png")