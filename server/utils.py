def cleanseAxieWalletData(data):
    """
    remove sensitive like username and password
    """
    return list(map(lambda axieWallet: { 
            "id": str(axieWallet["_id"]),
            "axieWalletAddr": axieWallet["axieWalletAddr"],
            "lenderAddress": axieWallet["lenderAddress"],
            "tokenIds": axieWallet["tokenIds"],
        }, data))
