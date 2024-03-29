import bittensor as bt
from PIL import Image, ImageDraw, ImageFont, ImageColor
from textwrap3 import wrap
import nltk
from loguru import logger
import files
import sys

NFTENSOR_DESCRIPTION = """NFTensor Text is a generative art project that generates NFTs from the first sentence of the Bittensor network's response to minter queries."""

def generate(query, query_id):
    print(f"query id is {query_id}")
    response = query_bittensor(query,query_id)
    short_response = get_first_sentence(response)
    image = draw_image(short_response)
    save_image(image, query_id, query, short_response)
    print(f"image number {query_id} is saved")

def query_bittensor(input,query_id):
    # load the ss58 prefix from the .env files
    print(f"querying bittensor for number {query_id}")
    resp = bt.prompt(input)
    print(resp)
    if resp is not None and resp != "":
        print(f"resp is not none for {query_id}")
        print(f"resp is{resp}for {query_id}")
        return resp
    else:
        return query_bittensor(input,query_id)
    """
    else:
        print("No response what on Earth happened")
        return query_bittensor(input)
    """

def draw_image(short_response):
    img = Image.open(files.get_base_image_path())
    draw = ImageDraw.Draw(img)
    width, height = img.size
    x = width // 2
    y = height // 2
    max_font_size = 200

    text_color = (255, 255, 255)

    font = None
    font_size = max_font_size
    line_spacing = 1.5
    
    if len(short_response) > 325:
        short_response = short_response[:325]

    print(short_response)
    while font_size > 0:
        font = ImageFont.truetype(files.get_font_path(), font_size)
        wrapped_text = wrap(
            short_response, width=int(width * 1.5 / font_size), break_long_words=False
        )
        line_heights = [
            draw.textbbox((0, 0), line, font=font)[3]
            - draw.textbbox((0, 0), line, font=font)[1]
            for line in wrapped_text
        ]
        print(line_heights)
        max_line_height = max(line_heights)
        total_height = sum(line_heights) + int(
            (len(wrapped_text) - 1) * max_line_height * (line_spacing - 1)
        )

        if total_height <= height * 0.8:
            break

        font_size -= 1

    if font is None:
        logger.error("text length exceeds maximum font size")
        return
    else:
        total_height = sum(line_heights) + int(
            (len(wrapped_text) - 1) * max_line_height * (line_spacing - 1)
        )
        y -= total_height // 2

        for line in wrapped_text:
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            line_height = line_bbox[3] - line_bbox[1]
            draw.text((x - line_width // 2, y), line, fill=text_color, font=font)
            y += int(max_line_height * line_spacing)

        return img


def save_image(image, query_id, input, output):
    logger.remove()
    logger.add(sys.stdout)
    image.save(files.IMAGE_OUT_PATH + f"{query_id}.png")
    if not files.image_exists(query_id):
        logger.debug(f"failed to generate image for query #{query_id}")
        files.cleanup(query_id)
        return
    else:
        logger.info(f"successfully generated image for query #{query_id}")
        files.generate_json(query_id, NFTENSOR_DESCRIPTION, input, output)

def get_first_sentence(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Return the first sentence
    if sentences:
        return sentences[0]
    else:
        return ""
