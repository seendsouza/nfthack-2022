from pymongo import MongoClient

"""
axie-wallets
[
  {
    "axieWalletAddress": String,
    "privateKey": Bytes,
    "lenderAddress": String,
    "tokenIds": [String],
    "isCurrentlyUsed": Boolean,
    "username": String,
    "password": String,
    "rentedAt": int (UNIX epoch),
    "renterAddress": String
  }
]
"""


def createAxieWallet(db, axieWalletAddr, privateKey, lenderAddress):
    """
    initialize axie wallet in database
    """
    db.axieWallets.insert_one(
        {
            "axieWalletAddress": axieWalletAddr,
            "privateKey": privateKey,
            "lenderAddress": lenderAddress,
            "tokenIds": [],
            "isCurrentlyUsed": False,
            "username": "",
            "password": "",
            "renterAddress": "",
        }
    )


def completeTransfer(db, axieWalletAddr, axies, username, password):
    """
    complete transfer of axies to axieWallet
    """
    db.axieWallets.update_one(
        {"axieWalletAddress": axieWalletAddr},
        {
            "$set": {
                "tokenIds": axies,
                "username": username,
                "password": password,
            }
        },
    )


def addAxiesToWallet(db, axieWalletAddr, axies):
    """
    add axies to axieWallet
    """
    db.axieWallets.update_one(
        {
            "axieWalletAddress": axieWalletAddr,
        },
        {"$push": {"tokenIds": {"$each": axies}}},
    )


def getAvailableAxieWallets(db, ownerWallet=None):
    """
    Returns a list of all AxieWallets
    if owner is specificed, only returns AxieWallets owned by that owner
    """
    if ownerWallet:
        return db.axieWallets.find({"lenderAddress": ownerWallet})
    else:
        return db.axieWallets.find()


def deleteAxieWallet(db, axieWallet):
    """
    deletes AxieWallet from database
    """
    db.axieWallets.delete_one({"axieWalletAddress": axieWallet})


def getAxieWallet(db, axieWallet):
    """
    gets one specific axieWallet from database
    """
    return db.axieWallets.find_one({"axieWalletAddress": axieWallet})


def rentAxiesWallet(db, axieWallet, renterAddress, time):
    """
    rent axies from axieWallet
    """
    db.axieWallets.update_one(
        {"axieWalletAddress": axieWallet},
        {
            "$set": {
                "renterAddress": renterAddress,
                "rentedAt": time,
                "isCurrentlyUsed": True,
            }
        },
    )


def stopUsingAxie(db, axieWallet):
    """
    stop using axieWallet
    """
    db.axieWallets.update_one(
        {"axieWalletAddress": axieWallet},
        {
            "$set": {
                "renterAddress": "",
                "rentedAt": 0,
                "isCurrentlyUsed": False,
            }
        },
    )


def setAxieRentedAtTime(db, axieWallet, rentedAt):
    """
    sets the rentedAt time of an axieWallet
    """
    db.axieWallets.update_one(
        {"axieWalletAddress": axieWallet}, {"$set": {"rentedAt": rentedAt}}
    )


def setAxieWalletUsage(db, axieWallet, axieWalletUsage):
    return db.axieWallets.update_one(
        {"axieWalletAddress": axieWallet},
        {"$set": {"isCurrentlyUsed": axieWalletUsage}},
    )


def getRentersAxieWallets(db, renterAddress):
    """
    Returns a list of AxieWallets that are rented by renterAddress
    """
    return db.axieWallets.find({"renterAddress": renterAddress})
