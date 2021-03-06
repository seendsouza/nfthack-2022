import random as rand
import string, time
from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from utils import cleanseAxieWalletData, createWallet, getAxiesIds, Wallet
from db import (
    getAvailableAxieWallets,
    deleteAxieWallet,
    createAxieWallet,
    addAxiesToWallet,
    getAxieWallet,
    setAxieWalletUsage,
    getRentersAxieWallets,
    rentAxiesWallet,
    completeTransfer,
    stopUsingAxie,
)
from w3Connect import returnAxiesToOwner

app = Flask(__name__)
CORS(app)
client = MongoClient("localhost", 27017)
db = client.axie

## Main Routes

# first start lending and initialize all the axie wallet stuff
# then, once the user has added all the axies to it, we can finish transfer


@app.route("/start-lending/<string:lenderWallet>", methods=["POST"])
def startLending(lenderWallet):
    """
    generate wallet
    """

    # TODO: This is not the correct flow. We generate the wallet, we show this wallet
    # TODO: to the lender. They send their axies into this wallet, then we are back
    # TODO: in this function

    newAxieWallet = createWallet()
    newAxieWalletAddr = "0x" + newAxieWallet.addr.hex()

    createAxieWallet(db, newAxieWalletAddr, newAxieWallet.private_key, lenderWallet)

    return jsonify(
        {
            "message": "started lending for " + lenderWallet,
            "axieWalletAddress": newAxieWalletAddr,
        }
    )


@app.route(
    "/finish-transfer/<string:lenderWallet>/<string:axieWallet>", methods=["POST"]
)
def finishTransfer(lenderWallet, axieWallet):
    """
    user has transferred axies to wallet, create axie account, update db with new data
    """

    # ! make sure the axieWallet is of the form: 0x3db763bbbb1ac900eb2eb8b106218f85f9f64a13
    axies = getAxiesIds(axieWallet)

    # TODO: create axie account and return axie account username/password
    (axieAccountUsername, axieAccountPassword) = (
        str(rand.randint(0, 100000)),
        str(rand.randint(0, 100000)),
    )

    completeTransfer(db, axieWallet, axies, axieAccountUsername, axieAccountPassword)

    return jsonify({"message": "finished transfer for " + lenderWallet})


@app.route("/return-axies/<string:axieWallet>")
def returnAxies(axieWallet):
    """
    return the axies to their original owner
    """

    axieWalletData = getAxieWallet(db, axieWallet)

    # wallet = Wallet(
    #     private_key=bytes(axieWalletData["privateKey"]),
    #     public_key=bytes(axieWalletData["axieWalletAddress"]),
    #     addr=bytes(axieWalletData["axieWalletAddress"]),
    # )

    # originalOwner = axieWalletData["lenderAddress"]

    # for axieId in axieWalletData["tokenIds"]:
    #     returnAxiesToOwner(wallet, axieId, originalOwner)

    # returnAxiesToOwner(wallet, originalOwner, axieId)

    # TODO: delete axie wallet and axie account?
    # ! ^ this is not Solana, you can't delete a wallet :)
    # * deleting account, though, makes a lot of sense.

    deleteAxieWallet(db, axieWallet)
    # return jsonify({"message": "returned axies to " + originalOwner})
    return jsonify({"message": "returned axies to originalOwner"})


@app.route("/list-lent-axies", defaults={"lenderAddress": None})
@app.route("/list-lent-axies/<string:lenderAddress>")
def listLentAxies(lenderAddress):
    """
    returns a list of all the lent axie wallets, aka get all axie wallets that are available to be borrowed

    if lenderAddress is given, returns only axie wallets that are from that lender
    """
    data = getAvailableAxieWallets(db, lenderAddress)
    cleanedData = cleanseAxieWalletData(list(data))

    return jsonify({"message": "list of axies lent out", "data": cleanedData})


@app.route("/rent-axies/<string:axieWallet>/<string:renterAddress>")
def rentAxies(axieWallet, renterAddress):
    """
    user rents axies, get axie account info (username, password), set axie wallet to be in use, set rented at date
    """
    wallet = getAxieWallet(db, axieWallet)
    rentAxiesWallet(db, axieWallet, renterAddress, int(time.time()))

    if wallet is None:
        return jsonify({"message": "axie wallet not found"})

    return jsonify(
        {
            "message": "axie account login info for " + axieWallet,
            "data": {
                "username": wallet["username"],
                "password": wallet[
                    "password"
                ],  # encrypted password??? it's fine, it's a hackathon
            },
        }
    )


@app.route("/stop-using-axie/<string:axieWallet>")
def stopUsingAxieRoute(axieWallet):
    """
    stop using axie account, set axie wallet to be available for other renters
    """
    stopUsingAxie(db, axieWallet)

    return jsonify({"message": "stopped using axie account"})


@app.route("/get-renter-axies/<string:renterAddress>")
def getRenterAxies(renterAddress):
    """
    get axies that are currently being rented by a given renter
    """
    data = getRentersAxieWallets(db, renterAddress)
    cleaned_data = cleanseAxieWalletData(data)

    return jsonify(
        {"message": "axies being rented by " + renterAddress, "data": cleaned_data}
    )


@app.route("/get-axies-in-wallet/<string:wallet>")
def getAxiesInWallet(wallet):
    """
    get axies all axies that are in a given wallet
    """

    if wallet is None or wallet == "undefined" or wallet == "" or wallet == "null":
        return jsonify({"message": "no wallet supplied"}), 400

    data = getAxiesIds(wallet)

    return jsonify({"message": "axies in wallet", "data": data})


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



@app.route("/fake-insert", defaults={"lenderAddress": None}, methods=["POST"])
@app.route("/fake-insert/<string:lenderAddress>", methods=["POST"])
def fakeInsert(lenderAddress):
    """
    insert fake data into db
    """
    if lenderAddress is None:
        db.axieWallets.insert_one(
            {
                "axieWalletAddress": "0x"
                + "".join(
                    rand.choice(
                        string.ascii_uppercase + string.ascii_lowercase + string.digits
                    )
                    for _ in range(32)
                ),
                "lenderAddress": "0x"
                + "".join(
                    rand.choice(
                        string.ascii_uppercase + string.ascii_lowercase + string.digits
                    )
                    for _ in range(32)
                ),
                "renterAddress": "",
                "username": "axie-username-" + str(rand.randint(0, 100000)),
                "password": "axie-password-" + str(rand.randint(0, 100000)),
                "tokenIds": [
                    str(rand.randint(0, 100000)),
                    str(rand.randint(0, 100000)),
                    str(rand.randint(0, 100000)),
                ],
                "isCurrentlyUsed": False,
                "rentedAt": rand.randint(0, 100000),
            }
        )
        return jsonify({"message": "inserted fake data"})
    else:
        db.axieWallets.insert_one(
            {
                "axieWalletAddress": "0x"
                + "".join(
                    rand.choice(
                        string.ascii_uppercase + string.ascii_lowercase + string.digits
                    )
                    for _ in range(32)
                ),
                "lenderAddress": lenderAddress,
                "renterAddress": "",
                "username": "axie-username-" + str(rand.randint(0, 100000)),
                "password": "axie-password-" + str(rand.randint(0, 100000)),
                "tokenIds": [
                    str(rand.randint(0, 100000)),
                    str(rand.randint(0, 100000)),
                    str(rand.randint(0, 100000)),
                ],
                "isCurrentlyUsed": False,
                "rentedAt": rand.randint(0, 100000),
            }
        )
        return jsonify({"message": "inserted fake data"})


if __name__ == "__main__":
    app.run(debug=True)
