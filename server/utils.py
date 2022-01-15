def cleanseAxieWalletData(data):
    """
    remove sensitive like username and password
    """
    return list(map(lambda axieWallet: { 
            "id": str(axieWallet["_id"]),
            "axieWalletAddress": axieWallet["axieWalletAddress"],
            "lenderAddress": axieWallet["lenderAddress"],
            "tokenIds": axieWallet["tokenIds"],
            "isCurrentlyUsed": axieWallet["isCurrentlyUsed"],
        }, data))
