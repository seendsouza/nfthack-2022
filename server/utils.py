def cleanseAxieWalletData(data):
    """
    remove sensitive like username and password
    """
    return list(map(lambda axieWallet: { 
            "wallet": axieWallet["wallet"], 
            "owner-wallet": axieWallet["owner-wallet"], 
            "contained-axies": axieWallet["contained-axies"]
        }, data))
