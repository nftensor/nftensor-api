import os
import json
IMAGE_OUT_PATH = "/execute/assets/imgs/out/"
METADATA_OUT_PATH = "/execute/assets/json/"



# handle creation of json metadata files
def generate_json(query_id, description, input, response):
    json_metadata = {
        "name": f"NFTensor Text #{query_id}",
        "description": description,
        "image": f"https://text.nftensor.com/images/{query_id}.png",
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

# check json exists
def json_exists(query_id):
    return os.path.isfile(METADATA_OUT_PATH + f"{query_id}")

# handle removal of created files
def remove_image(query_id):
    try:
        os.remove(IMAGE_OUT_PATH + f"{query_id}.png")
    except OSError:
        pass


def remove_metadata(query_id):
    try:
        os.remove(METADATA_OUT_PATH + f"{query_id}")
    except OSError:
        pass


def cleanup(query_id):
    remove_image(query_id)
    remove_metadata(query_id)


