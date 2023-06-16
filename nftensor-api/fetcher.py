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
    event_filter = contract.events.Transfer.createFilter(fromBlock="latest")

    start_time = time.time()
    while True:
        events = event_filter.get_new_entries()
        for event in events:
            print(event)
            if event.args["from"] == "0x0000000000000000000000000000000000000000":
                handle_event(w3, contract, event)

        if time.time() - start_time > 500:
            check_for_mints(contract)
            start_time = time.time()


def check_for_mints(contract):
    # get a singular query
    for i in range(1, 501):
        handle_mint(contract, i)

def handle_mint(contract, id):
        query = contract.functions.queries(id).call()
        if not files.image_exists(id):
            if query != "":
                logger.info(f"new query found, re-generating image #{id}")
                generator.generate(query, id)
        else:
            # we have to fix this
            if files.json_exists(id):
                with open(f"/execute/assets/json/{id}", "r") as f:
                    data = json.load(f)
                    if query != data["attributes"][0]["value"]:
                        logger.warn("re-org found, re-generating image")
                        generator.generate(query, id)
            else:
                logger.warn("image exists, but json not generated, cleaning up for retry")
                files.cleanup(id)

def handle_event(provider, contract, event):
    txn_hash = provider.eth.waitForTransactionReceipt(event["transactionHash"])
    # check if the sender is 0 
    print(txn_hash)
    id = contract.functions.tokenID().call() 
    handle_mint(contract, id)
