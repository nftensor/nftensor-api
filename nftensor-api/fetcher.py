from web3 import Web3
import abi
import generator
from loguru import logger
import time


# fetches queries from the NFTensor contract
def fetch_queries(endpoint, nftensor_address):
    # connect to the blockchain
    # w3 = Web3(Web3.HTTPProvider(endpoint))
    w3 = Web3(Web3.WebsocketProvider("ws://localhost:8545"))
    # get the contract
    contract = w3.eth.contract(address=nftensor_address, abi=abi.nftensor_abi)
    event_filter = contract.events.Transfer.createFilter(fromBlock="latest")
    block_filter = w3.eth.filter({"fromBlock": "latest", "address": nftensor_address})

    start_time = time.time()
    while True:
        events = block_filter.get_new_entries()
        for event in events:
            handle_event(w3, event)

        if time.time() - start_time > 500:
            check_for_mints()
            start_time = time.time()


def check_for_mints():
    # get a singular query
    for i in range(1, 501):
        query = contract.functions.queries(i).call()
        if generator.image_exists(i):
            if query != "":
                logger.info(f"new query found, re-generating image #{i}")
                generator.generate_image(query, i)
        else:
            with open("./assets/json/{i}.json", "r") as f:
                data = json.load(f)
                if query != data["attributes"][0]["value"]:
                    logger.warn("re-org found, re-generating image")
                    generator.generate_image(query, i)


def handle_event(provider, event):
    txn_hash = provider.eth.waitForTransactionReceipt(event["transactionHash"])
