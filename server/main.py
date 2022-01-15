import random as rand
from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from utils import cleanseAxieWalletData
from db import getAvailableAxieWallets, deleteAxieWallet, createAxieWallet, addAxiesToWallet, getAxieWallet
from w3Connect import getAxiesInWallet, returnAxiesToOwner

app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client.axie

@app.route("/start-lending/<string:lenderWallet>")
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
            "axieWalletAddr": newAxieWalletAddr
        })

@app.route("/finish-transfer/<string:lenderWallet>/<string:axieWallet>")
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

@app.route("/use-axie-account/<string:axieWallet>")
def useAxieAccount(axieWallet):
    """
    get axie account login info
    """
    wallet = getAxieWallet(db, axieWallet)

    if wallet is None:
        return jsonify({"message": "axie wallet not found"})

    return jsonify({
        "message": "axie account login info for " + axieWallet,
            "data": {
                "username": wallet["username"],
                "password": wallet["password"] # encrypted password??? it's fine, it's a hackathon
            }
        })

@app.route("/clear-all")
def clearAll():
    """
    clear all data from db
    """
    db.axieWallets.delete_many({})
    return jsonify({"message": "cleared all data"})

if __name__ == '__main__':
    app.run(debug=True)


