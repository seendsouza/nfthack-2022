# Developer Guide

1. Use python==3.8.12
2. pip install -r requirements.txt

## API responses

1. GET https://game-api.axie.technology/api/v1/0x0000000000000000000000000000000000000000

returns

```json
{
  "success": true,
  "cache_last_updated": 1642254489593,
  "draw_total": 0,
  "lose_total": 0,
  "win_total": 0,
  "total_matches": 0,
  "win_rate": 0,
  "mmr": 1200,
  "rank": 2147483647,
  "ronin_slp": 0,
  "total_slp": 0,
  "raw_total": 0,
  "in_game_slp": 0,
  "last_claim": 0,
  "lifetime_slp": 0,
  "name": null,
  "next_claim": 1209600
}
```

2. https://stackoverflow.com/questions/69908168/where-can-i-learn-more-about-api-in-axie-infinity

To return list of axies that someone has:

```python
url = 'https://graphql-gateway.axieinfinity.com/graphql'

def get_axie_ids(ronin_address):
query_all_axie_ids = {
    "operationName": "GetAxieLatest",
    "variables": {
        'owner': ronin_address
    },
    "query": "query GetAxieLatest($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieRowData\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieRowData on Axie {\n  id\n  image\n  class\n  name\n  genes\n  owner\n  class\n  stage\n  title\n  breedCount\n  level\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
}
r = requests.post(url, json = query_all_axie_ids)
axies = []
for x in range(0, len(r.json()['data']['axies']['results'])):
    axies.append(r.json()['data']['axies']['results'][x]['id'])

return axies
```

Details of each Axie, given its id

```python
def get_axie(axie_id):
query_axie = {
    "operationName": "GetAxieDetail",
    "variables": {
        "axieId": axie_id
    },
    "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
}

r = requests.post(url, json = query_axie)
axie = r.json()['data']

return axie
```

3. Complete but not official documentation here

https://axie-graphql.web.app/
