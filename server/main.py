from flask import Flask, jsonify

app = Flask(__name__)


# currently setup to return dummy data for all routes

@app.route("/start-lending/<string:ownerWallet>")
def startLending(ownerWallet):
    """
    generate wallet, transfer axie to wallet, create axie account
    """
    return jsonify({"message": "started lending for " + ownerWallet})

@app.route("/return-axies/<string:wallet>")
def returnAxies(wallet):
    """
    return the axies to their original owner
    """
    return jsonify({"message": "returned axies to " + wallet})

@app.route("/list-lent-axies")
def listListAxies():
    """
    returns a list of all the axies that are lent out
    """
    return jsonify({
            "message": "list of axies lent out",
            "data": ["0x06012c8cf97BEaD5deAe237070F9587f8E7A266d", "0x06012c8cf97BEaD5deAe237070F9587f8E7A266d"]
        })

@app.route("/use-axie-account/<string:accountId>")
def useAxieAccount(accountId):
    """
    get axie account login info
    """
    return jsonify({
        "message": "axie account login info: " + accountId,
            "data": {
            "username": "axie-username",
            "password": "axie-password" # encrypted password??? it's fine, it's a hackathon
            }
        })

if __name__ == '__main__':
    app.run(debug=True)


