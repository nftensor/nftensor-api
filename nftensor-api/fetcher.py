from web3 import Web3 
import abi

# fetches queries from the NFTensor contract 
def fetch_queries(endpoint, nftensor_address):
    # connect to the blockchain
    w3 = Web3(Web3.HTTPProvider(endpoint))
    # get the contract
    contract = w3.eth.contract(address=nftensor_address, abi=abi.nftensor_abi)

    print(abi.nftensor_abi)
