from web3 import Web3
import abi
import files
import generator
from loguru import logger
import time
import json


# fetches queries from the NFTensor contract
def fetch_queries(endpoint, nftensor_address):
    # connect to the blockchain
    w3 = Web3(Web3.WebsocketProvider(endpoint))
    # get the contract
    contract = w3.eth.contract(address=nftensor_address, abi=abi.nftensor_abi)

    while True:

        check_for_mints(contract)
        print("checked for mints")

def check_for_mints(contract):
    # get a singular query
    for i in range(1, 501):
        handle_mint(contract, i)

def handle_mint(contract, id):
    query = contract.functions.queries(id).call()
    if query != "":
        if not files.image_exists(id):
                logger.info(f"new query found, generating image #{id}")
                generator.generate(query, id)
        else:
            if files.json_exists(id):
                with open(f"/execute/assets/json/{id}", "r") as f:
                    data = json.load(f)
                    if query != data["attributes"][0]["value"]:
                        logger.warn("re-org found, re-generating image")
                        generator.generate(query, id)
            else:
                logger.warn("image exists, but json not generated, cleaning up for retry")
                files.cleanup(id)
