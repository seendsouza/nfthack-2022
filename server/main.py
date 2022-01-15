import random as rand
import string, time
from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from utils import cleanseAxieWalletData
from db import getAvailableAxieWallets, deleteAxieWallet, createAxieWallet, addAxiesToWallet, \
    getAxieWallet, setAxieWalletUsage, getRentersAxieWallets, setAxieRentedAtTime
from w3Connect import getAxiesInWallet, returnAxiesToOwner

app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client.axie

@app.route("/start-lending/<string:lenderWallet>", methods=['POST'])
def startLending(lenderWallet):
    """
    generate wallet, create axie account
    """

    # TODO: create ronin wallet to store axies
    newAxieWalletAddr = str(rand.randint(0, 1000000))
    # TODO: create axie account
    (axieAccountUsername, axieAccountPassword) = (str(rand.randint(0, 100000)), str(rand.randint(0, 100000)))

    createAxieWallet(db, newAxieWalletAddr, lenderWallet, axieAccountUsername, axieAccountPassword)

    return jsonify({
            "message": "started lending for " + lenderWallet,
            "axieWalletAddress": newAxieWalletAddr
        })

@app.route("/finish-transfer/<string:lenderWallet>/<string:axieWallet>" , methods=['POST'])
def finishTransfer(lenderWallet, axieWallet):
    """
    user has transfered axies to account, update db with new data
    """

    # TODO: get axies in wallet
    axies = getAxiesInWallet(lenderWallet)

    addAxiesToWallet(db, axieWallet, axies)

    return jsonify({"message": "finished transfer for " + lenderWallet})

@app.route("/return-axies/<string:axieWallet>")
def returnAxies(axieWallet):
    """
    return the axies to their original owner
    """

    originalOwner = getAxieWallet(db, axieWallet)["lenderAddress"]

    # TODO: return axies to original owner
    returnAxiesToOwner(axieWallet, originalOwner)

    deleteAxieWallet(db, axieWallet) 
    return jsonify({"message": "returned axies to " + originalOwner})

@app.route("/list-lent-axies", defaults={"lenderAddress": None})
@app.route("/list-lent-axies/<string:lenderAddress>")
def listLentAxies(lenderAddress):
    """
    returns a list of all the axie wallets that are available to be borrowed and belong to the given owner
    """
    data = getAvailableAxieWallets(db, lenderAddress)
    cleanedData = cleanseAxieWalletData(list(data))

    return jsonify({
            "message": "list of axies lent out",
            "data": cleanedData
        })

@app.route("/get-axie-account-info/<string:axieWallet>")
def getAxieAccountInfo(axieWallet):
    """
    user rents axies, get axie account info (username, password), set axie wallet to be in use, set rented at date
    """
    wallet = getAxieWallet(db, axieWallet)
    setAxieWalletUsage(db, axieWallet, True)
    setAxieRentedAtTime(db, axieWallet, int(time.time()))

    if wallet is None:
        return jsonify({"message": "axie wallet not found"})

    return jsonify({
        "message": "axie account login info for " + axieWallet,
            "data": {
                "username": wallet["username"],
                "password": wallet["password"] # encrypted password??? it's fine, it's a hackathon
            }
        })

@app.route("/stop-using-axie/<string:axieWallet>")
def stopUsingAxie(axieWallet):
    """
    stop using axie account
    """
    setAxieWalletUsage(db, axieWallet, False)

    return jsonify({"message": "stopped using axie account"})

@app.route("/get-renter-axies/<string:renterAddress>")
def getRenterAxies(renterAddress):
    """
    get axies that are currently being rented
    """
    data = getRenterAxies(db, renterAddress)
    cleaned_data = cleanseAxieWalletData(axies)

    return jsonify({
            "message": "axies being rented by " + renterAddress,
            "data": cleaned_data
        })

############################################################################################
## these are for testing/dev purposes
############################################################################################
@app.route("/clear-all")
def clearAll():
    """
    clear all data from db
    """
    db.axieWallets.delete_many({})
    return jsonify({"message": "cleared all data"})

@app.route("/fake-insert", methods=['POST'])
def fakeInsert():
    """
    insert fake data into db
    """
    db.axieWallets.insert_one({
        "axieWalletAddress": "0x" +  ''.join(rand.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32)),
        "lenderAddress": "0x" + ''.join(rand.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32)),
        "username": "axie-username-"+str(rand.randint(0, 100000)),
        "password": "axie-password-"+str(rand.randint(0, 100000)),
        "tokenIds": [str(rand.randint(0, 100000)), str(rand.randint(0, 100000)), str(rand.randint(0, 100000))],
        "isCurrentlyUsed": False
    })
    return jsonify({"message": "inserted fake data"})


if __name__ == '__main__':
    app.run(debug=True)


