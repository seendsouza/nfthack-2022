from dataclasses import dataclass
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256

@dataclass(frozen=True)
class Wallet():
    private_key: bytes
    public_key: bytes
    addr: bytes

def cleanseAxieWalletData(data):
    """
    remove sensitive like username and password
    """
    return list(map(lambda axieWallet: { 
            "id": str(axieWallet["_id"]),
            "axieWalletAddress": axieWallet["axieWalletAddress"],
            "lenderAddress": axieWallet["lenderAddress"],
            "tokenIds": axieWallet["tokenIds"],
            "isCurrentlyUsed": axieWallet["isCurrentlyUsed"],
            "rentedAt": axieWallet["rentedAt"],
        }, data))

# source: https://www.arthurkoziel.com/generating-ethereum-addresses-in-python/
def createWallet() -> Wallet:
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]

    # print('private_key:', private_key.hex())
    # print('eth addr: 0x' + addr.hex())

    ### Output (Random each time) ###
    # private_key: 7bf19806aa6d5b31d7b7ea9e833c202e51ff8ee6311df6a036f0261f216f09ef
    # eth addr: 0x3db763bbbb1ac900eb2eb8b106218f85f9f64a13

    return Wallet(private_key, public_key, addr)
