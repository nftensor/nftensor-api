import bittensor as bt
from PIL import Image, ImageDraw, ImageFont, ImageColor
from textwrap3 import wrap
import nltk
import os
import json
from pinatapy import PinataPy
from dotenv import load_dotenv
from loguru import logger

NFTENSOR_DESCRIPTION = """NFTensor Text is a generative art project that generates NFTs from the first sentence of the Bittensor network's response to minter queries"""


def query_bittensor(input):
    # load the ss58 prefix from the .env files
    load_dotenv()
    ss58 = os.getenv("BITTENSOR_SS58")

    try:
        resp = bt.prompt(input, hotkey=ss58)
    except:
        logger.warn("failed to query bittensor")
        resp = None

    if resp is not None:
        return resp
    else:
        return ""


def generate_image(query, query_id):
    # query bittensor and grab the first sentence of the response
    response = query_bittensor(query)
    response = query_bittensor(input, query_id)
    if resp == "":
        return
    short_response = get_first_sentence(response)

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
        max_line_height = max(line_heights)
        total_height = sum(line_heights) + int(
            (len(wrapped_text) - 1) * max_line_height * (line_spacing - 1)
        )

        if total_height <= height * 0.8:
            break

        font_size -= 1

    if font is None:
        logger.error("text length exceeds maximum font size")
        # add error handling
        # what should we do here?
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

        save_image(img, query_id, query, short_response)


def save_image(image, query_id, input, output):
    image.save(f"./assets/imgs/out/{query_id}.png")
    if not image_exists(query_id):
        logger.debug(f"failed to generate image for query #{query_id}")
        files.cleanup(query_id)
        return
    else:
        logger.info(f"successfully generated image for query #{query_id}")
        try:
            img_hash = files.upload_image(query_id)
        except:
            files.cleanup(query_id)
            return

        files.generate_json(query_id, NFTENSOR_DESCRIPTION, img_hash, input, output)


def get_first_sentence(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Return the first sentence
    if sentences:
        return sentences[0]
    else:
        return ""
