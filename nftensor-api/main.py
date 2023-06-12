import generator
import fetcher
import os
import dotenv
from logguru import logger


def main():
    logger.info("Starting NFTensor")
    # load .env
    dotenv.load_dotenv()
    endpoint = os.getenv("ENDPOINT")
    nftensor_address = os.getenv("NFTENSOR_ADDRESS")
    fetcher.fetch_queries(endpoint, nftensor_address)


if __name__ == "__main__":
    main()
