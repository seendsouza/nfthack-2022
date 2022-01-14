from pymongo import MongoClient

"""
axie-wallets
[
  {
    "wallet": String,
    "owner-wallet": String,
    "contained-axies": [String],
    "username": String,
    "password": String,
  }
]
"""

def createAxieWallet(db, wallet, ownerWallet, username, password):
    db.axieWallets.insertOne({"wallet": wallet, "owner-wallet": ownerWallet, "contained-axies": [], "username": username, "password": password})

def addAxiesToWallet(db, axieWallet, axies):
    db.axieWallets.updateOne({"wallet": axieWallet,}, {"$push": {"contained-axies": {"$each": axies}}})

def getAvailableAxieWallets(db):
    return db.axieWallets.find()

def getAvailableAxieWallets(db, ownerWallet):
    return db.axieWallets.find({"owner-wallet": ownerWallet})

def deleteAxieWallet(db, axieWallet):
    db.axieWallets.deleteOne({"wallet": axieWallet})

def getAxieWallet(db, axieWallet):
    return db.axieWallets.findOne({"wallet": axieWallet})
