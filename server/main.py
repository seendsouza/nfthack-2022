from flask import Flask

app = Flask(__name__)

@app.route("/start-lending")
def startLending():
    """
    generate wallet, transfer axie to wallet, create axie account
    """
    return "Hello World!"

@app.route("/return-axies")
def returnAxies():
    """
    return the axies to their original owner
    """
    return "Hello World!"

@app.route("/list-lent-axies")
def listListAxies():
    """
    returns a list of all the axies that are lent out
    """
    return "Hello World!"

@app.route("/use-axie-account")
def useAxieAccount():
    """
    get axie account login info
    """
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)


