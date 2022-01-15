import random as rand
from web3 import Web3

def getAxiesInWallet(walletAddress):
    methodSignature = Web3.sha3(text="balanceOf(address)").hex()[0:10]
    padding = "000000000000000000000000"
    data = methodSignature + padding + walletAddress[2:]

    #print(data)

    # body = {
    #     "method": "ethCall",
    #     "id": 1,
    #     "jsonrpc": "2.0",
    #     "params": [{"to": tokenAddress, "data": data}, "latest"],
    # }

    # url = "https://cloudflare-eth.com/"
    return [str(rand.randint(10001, 50000)), str(rand.randint(10001, 50000)), str(rand.randint(10001, 50000))]

def returnAxiesToOwner(axieWalletAddr, ownerWalletAddr):
    """
    return axies in axieWalletAddr back to owner
    """

# getAxiesInWallet("0x3D21FeAf3E1fE43d33cB3D0b3806B178Be953E49")
