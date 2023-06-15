import os
from pinatapy import PinataPy
import json
import dotenv

IMAGE_OUT_PATH = "/execute/assets/imgs/out/"
METADATA_OUT_PATH = "/execute/assets/json/"


# handle upload to ipfs
def upload_image(query_id):
    # load pinata api keys
    dotenv.load_dotenv()
    api_key = os.getenv("PINATA_API_KEY")
    secret = os.getenv("PINATA_API_SECRET_KEY")

    # open image to upload
    image_path = os.path.abspath(IMAGE_OUT_PATH + f"{query_id}.png")
    img = open(image_path, "r")

    # create pinata instance and upload to pinata
    pinata = PinataPy(pinata_api_key=api_key, pinata_secret_api_key=secret)
    pinata_response = pinata.pin_file_to_ipfs(image_path, save_absolute_paths=False)

    # return ipfs hash
    return pinata_response["IpfsHash"]


# handle creation of json metadata files
def generate_json(query_id, description, image_hash, input, response):
    json_metadata = {
        "name": f"NFTensor Text #{query_id}",
        "description": description,
        "image": f"ipfs://{image_hash}",
        "attributes": [
            {"trait_type": "query", "value": f"{input}"},
            {"trait_type": "response", "value": f"{response}"},
        ],
    }

    with open(METADATA_OUT_PATH + f"{query_id}", "w") as outfile:
        json.dump(json_metadata, outfile)


def get_base_image_path():
    return "/execute/assets/imgs/base/background_4k.png"


def get_font_path():
    return "/execute/assets/fonts/EBGaramond-Regular.ttf"


# check file exists
def image_exists(query_id):
    return os.path.isfile(IMAGE_OUT_PATH + f"{query_id}.png")


# handle removal of created files
def remove_image(query_id):
    os.remove(IMAGE_OUT_PATH + f"{query_id}.png")


def remove_metadata(query_id):
    os.remove(METADATA_OUT_PATH + f"{query_id}")


def cleanup(query_id):
    remove_image(query_id)
    remove_metadata(query_id)
