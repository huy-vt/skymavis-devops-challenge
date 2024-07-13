import requests
from prometheus_client import start_http_server, Gauge

INFURA_URL = "https://mainnet.infura.io/v3/8204320355b942fdb791bf5d33e269c4" 
ANKR_URL = "https://rpc.ankr.com/eth"

block_difference = Gauge('block_difference', 'Difference in block numbers between Ankr and Infura')
block_status = Gauge('block_status', 'if Ankr blocknumber - Infura blocknumber < 5 => success(1) - else => fail(0) .')
def fetch_block_number(url):
    try:
        response = requests.post(url, json={
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        })
        response.raise_for_status()
        result = response.json().get("result")
        return int(result, 16) if result else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching block number from {url}: {e}")
        return None

def main():
    start_http_server(8000)
    
    while True:
        infura_block = fetch_block_number(INFURA_URL)
        ankr_block = fetch_block_number(ANKR_URL)
        
        if infura_block is not None and ankr_block is not None:
            difference = infura_block - ankr_block
            block_difference.set(difference)            
            if difference < 5:
                block_status.set(int(1))
            else:
                block_status.set(int(0))
        
if __name__ == '__main__':
    main()