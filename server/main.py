from flask import Flask, jsonify
from pymongo import MongoClient
from utils import cleanseAxieWalletData
from db import getAvailableAxieWallets, deleteAxieWallet, createAxieWallet, addAxiesToWallet
from w3Connect import getAxiesInWallet, returnAxiesToOwner

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.axie

@app.route("/start-lending/<string:ownerWallet>")
def startLending(ownerWallet):
    """
    generate wallet, create axie account
    """

    # TODO: create ronin wallet to store axies
    axieWalletAddr = ""
    # TODO: create axie account
    (axieAccountUsername, axieAccountPassword) = ("", "")

    createAxieWallet(db, axieWalletAddr, ownerWallet, axieAccountUsername, axieAccountPassword)

    return jsonify({
            "message": "started lending for " + ownerWallet,
            "wallet": newAxieWalletAddr
        })

@app.route("/finish-transfer/<string:ownerWallet>/<string:axieWallet>")
def finishTransfer(ownerWallet, axieWallet):
    """
    user has transfered axies to account, update db with new data
    """

    # TODO: get axies in wallet
    axies = getAxiesInWallet(ownerWallet)

    addAxiesToWallet(db, axieWallet, axies)

    return jsonify({"message": "finished transfer for " + ownerWallet})

@app.route("/return-axies/<string:axieWallet>")
def returnAxies(axieWallet):
    """
    return the axies to their original owner
    """

    # TODO: return axies to original owner
    returnAxiesToOwner(axieWallet, originalOwner)

    deleteAxieWallet(db, axieWallet) 
    return jsonify({"message": "returned axies to " + wallet})

@app.route("/list-lent-axies", defaults={"ownerWallet": None})
@app.route("/list-lent-axies/<string:ownerWallet>")
def listLentAxies(ownerWallet):
    """
    returns a list of all the axie wallets that are available to be borrowed and belong to the given owner
    """
    data = getAvailableAxieWallets(db, ownerWallet)
    cleanedData = cleanseAxieWalletData(data)

    return jsonify({
            "message": "list of axies lent out",
            "data": cleanedData
        })

@app.route("/use-axie-account/<string:axieWallet>")
def useAxieAccount(axieWallet):
    """
    get axie account login info
    """
    wallet = getAxieWallet(db, axieWallet)
    return jsonify({
        "message": "axie account login info: " + wallet,
            "data": {
                "username": wallet["username"],
                "password": wallet["password"] # encrypted password??? it's fine, it's a hackathon
            }
        })

if __name__ == '__main__':
    app.run(debug=True)


