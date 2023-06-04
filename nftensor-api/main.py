import generator
import fetcher
import os
import dotenv 


def main():
    # load .env
    dotenv.load_dotenv()   
    endpoint = os.getenv("ENDPOINT")
    nftensor_address = os.getenv("NFTENSOR_ADDRESS")
    fetcher.fetch_queries(endpoint, nftensor_address)
    generator.generate_image("What is a solid gold magikarp")

if __name__ == '__main__':
    main()
