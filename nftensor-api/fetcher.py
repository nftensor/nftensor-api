from web3 import Web3 
import abi
import generator 
from loguru import logger

# fetches queries from the NFTensor contract 
def fetch_queries(endpoint, nftensor_address):
    # connect to the blockchain
    w3 = Web3(Web3.HTTPProvider(endpoint))
    # get the contract
    contract = w3.eth.contract(address=nftensor_address, abi=abi.nftensor_abi)

    # get a singular query 
    for i in range(1, 501):
        query = contract.functions.queries(i).call()
        if query != "" and not generator.image_exists(i):
            generator.generate_image(query, i)
        else:
            logger.info("no new queries found")
        
        
        
