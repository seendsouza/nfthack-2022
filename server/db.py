from pymongo import MongoClient

"""
axie-wallets
[
  {
    "axieWalletAddr": String,
    "lenderAddress": String,
    "tokenIds": [String],
    "username": String,
    "password": String,
  }
]
"""

def createAxieWallet(db, axieWalletAddr, lenderAddress, username, password):
    db.axieWallets.insert_one({"axieWalletAddr": axieWalletAddr, "lenderAddress": lenderAddress, "tokenIds": [], "username": username, "password": password})

def addAxiesToWallet(db, axieWalletAddr, axies):
    db.axieWallets.update_one({"axieWalletAddr": axieWalletAddr,}, {"$push": {"tokenIds": {"$each": axies}}})

def getAvailableAxieWallets(db, ownerWallet = None):
    if ownerWallet:
        return db.axieWallets.find({"lenderAddress": ownerWallet})
    else:
        return db.axieWallets.find()

def deleteAxieWallet(db, axieWallet):
    db.axieWallets.delete_one({"axieWalletAddr": axieWallet})

def getAxieWallet(db, axieWallet):
    return db.axieWallets.find_one({"axieWalletAddr": axieWallet})
