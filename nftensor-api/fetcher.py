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
    last_minted = get_last_minted()
    while True:
        
        check_for_mints(last_minted, contract)
        print("checked for mints")


def get_last_minted():
    last_minted = 0
    while files.image_exists(last_minted):
        last_minted += 1

    return last_minted

def check_for_mints(last_minted, contract):
    # get a singular query
    current_token_id = contract.functions.tokenID().call()
    if current_token_id > last_minted:
        for id in range(last_minted + 1, current_token_id + 1):
            handle_mint(contract, id)

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
