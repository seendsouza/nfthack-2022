from dataclasses import dataclass
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
import requests

AXIES_API = "https://graphql-gateway.axieinfinity.com/graphql"


@dataclass(frozen=True)
class Wallet:
    private_key: bytes
    public_key: bytes
    addr: bytes


def cleanseAxieWalletData(data):
    """
    remove sensitive like username and password
    """
    return list(
        map(
            lambda axieWallet: {
                "id": str(axieWallet["_id"]),
                "axieWalletAddress": axieWallet["axieWalletAddress"],
                "lenderAddress": axieWallet["lenderAddress"],
                "tokenIds": axieWallet["tokenIds"],
                "isCurrentlyUsed": axieWallet["isCurrentlyUsed"],
                "rentedAt": axieWallet["rentedAt"],
            },
            data,
        )
    )


# source: https://www.arthurkoziel.com/generating-ethereum-addresses-in-python/
def createWallet() -> Wallet:
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]

    # print('private_key:', private_key.hex())
    # print('eth addr: 0x' + addr.hex())

    ### Output (Random each time) ###
    # private_key: 7bf19806aa6d5b31d7b7ea9e833c202e51ff8ee6311df6a036f0261f216f09ef
    # eth addr: 0x3db763bbbb1ac900eb2eb8b106218f85f9f64a13

    return Wallet(private_key, public_key, addr)


# TODO: only returns 20 axies. Checked on: 0x7a904e39c0adf17f89da54a8edc7dc031fa4281a.
# TODO: The address above has 38 axies, but only 20 are returned.
# TODO: if you make a raw POST request in Postman, you will see that ['data']['axies']['total'] is correct at 38
# TODO: and the answer to the above is here: https://axie-graphql.web.app/operations/getAxieLatest#size
# TODO: we will need to paginate
# ronin address should be of the following format: 0x3db763bbbb1ac900eb2eb8b106218f85f9f64a13
def getAxiesIds(ronin_address: str):
    axies = []
    query_all_axie_ids = {
        "operationName": "GetAxieLatest",
        "variables": {"owner": ronin_address},
        "query": "query GetAxieLatest($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieRowData\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieRowData on Axie {\n  id\n  image\n  class\n  name\n  genes\n  owner\n  class\n  stage\n  title\n  breedCount\n  level\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n",
    }

    r = requests.post(AXIES_API, json=query_all_axie_ids)

    for x in range(0, len(r.json()["data"]["axies"]["results"])):
        axies.append(r.json()["data"]["axies"]["results"][x]["id"])

    return axies
