from web3 import Web3

from vendor.axie_utilities.axie.transfers import Transfer
from utils import Wallet

# WRITE TO RONIN

# ! wallets should be of the form: 0x3D21FeAf3E1fE43d33cB3D0b3806B178Be953E49
def returnAxiesToOwner(axieWallet: Wallet, ownerWalletAddr: str, axieId: int):
    """
    return axies in axieWalletAddr back to ownerWalletAddr
    """

    transfer = Transfer('0x' + axieWallet.addr.hex(), axieWallet.private_key, ownerWalletAddr, axieId)

    transfer.execute()
