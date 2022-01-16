import requests
from dataclasses import dataclass
from sha3 import keccak_256
from secrets import token_bytes
from coincurve import PublicKey
from web3.auto import w3
from eth_account.messages import encode_defunct

GRAPHQL_GATEWAY = "https://graphql-gateway.axieinfinity.com/graphql"
REGISTER_CAPTCHA = "https://captcha.axieinfinity.com/api/geetest/register"


@dataclass(frozen=True)
class Wallet:
    private_key: bytes
    public_key: bytes
    addr: bytes


def create_wallet() -> Wallet:
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(
        private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]
    return Wallet(private_key, public_key, addr)


def sign_message(message: str, wallet: Wallet):
    message = encode_defunct(text=message)
    signed_message = w3.eth.account.sign_message(
        message, private_key=wallet.private_key)
    return str(signed_message.signature.hex())


class AxieInfinity():
    def __init__(self, wallet):
        self.wallet = wallet
        self.bearer_token = None

    def create_random_message(self) -> str:
        create_random_message_body = {"operationName": "CreateRandomMessage", "variables": {
        }, "query": "mutation CreateRandomMessage {\n  createRandomMessage\n}\n"}
        res = requests.post(GRAPHQL_GATEWAY, json=create_random_message_body)

        message = res.json()['data']['createRandomMessage']
        return message

    def create_access_token_with_signature(self, message: str, signature: str) -> str:
        create_access_token_with_signature_body = {"operationName": "CreateAccessTokenWithSignature", "variables": {"input": {"mainnet": "ronin", "owner": "0x" + str(self.wallet.addr.hex(
        )), "message": message, "signature": signature}}, "query": "mutation CreateAccessTokenWithSignature($input: SignatureInput!) {\n  createAccessTokenWithSignature(input: $input) {\n    newAccount\n    result\n    accessToken\n    __typename\n  }\n}\n"}

        res = requests.post(
            GRAPHQL_GATEWAY, json=create_access_token_with_signature_body)

        access_token = res.json(
        )['data']['createAccessTokenWithSignature']['accessToken']
        bearer_token = "Bearer {}".format(access_token)
        self.bearer_token = bearer_token
        return access_token

    def get_profile_brief(self):
        get_profile_brief_body = {"operationName": "GetProfileBrief", "variables": {
        }, "query": "query GetProfileBrief {\n  profile {\n    ...ProfileBrief\n    __typename\n  }\n}\n\nfragment ProfileBrief on AccountProfile {\n  accountId\n  addresses {\n    ...Addresses\n    __typename\n  }\n  email\n  activated\n  name\n  settings {\n    unsubscribeNotificationEmail\n    __typename\n  }\n  __typename\n}\n\nfragment Addresses on NetAddresses {\n  ethereum\n  tomo\n  loom\n  ronin\n  __typename\n}\n"}

        res = requests.post(
            GRAPHQL_GATEWAY, headers={"Authorization": self.bearer_token}, json=get_profile_brief_body)
        return res.json()

    def update_profile_name(self, name: str):
        update_profile_name_body = {"operationName": "UpdateProfileName", "variables": {"name": name},
                                    "query": "mutation UpdateProfileName($name: String!) {\n  updateProfileName(name: $name) {\n    accountProfile {\n      ...ProfileBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileBrief on AccountProfile {\n  accountId\n  addresses {\n    ...Addresses\n    __typename\n  }\n  email\n  activated\n  name\n  settings {\n    unsubscribeNotificationEmail\n    __typename\n  }\n  __typename\n}\n\nfragment Addresses on NetAddresses {\n  ethereum\n  tomo\n  loom\n  ronin\n  __typename\n}\n"}

        res = requests.post(
            GRAPHQL_GATEWAY, headers={"Authorization": self.bearer_token}, json=update_profile_name_body)
        return res.json()


def main():

    email = "john@example.com"
    wallet = create_wallet()

    ai = AxieInfinity(wallet)

    message = ai.create_random_message()

    signature = sign_message(message, wallet)

    print("Message: ", message)
    print("Signature: ", signature)

    access_token = ai.create_access_token_with_signature(message, signature)
    bearer_token = "Bearer {}".format(access_token)
    print("Access Token: ", access_token)

    profile_brief = ai.get_profile_brief()

    print(profile_brief)

    # TODO: Do captcha

    """
    captcha_token: {"geetest_challenge": "", "geetest_validate": "", "geetest_seccode": ""}
    verify_email_body = {"operationName": "VerifyEmail", "variables": {"email": email},
                         "query": "mutation VerifyEmail($email: String!) {\n  verifyEmail(email: $email) {\n    result\n    __typename\n  }\n}\n"}

    res = requests.post(
        GRAPHQL_GATEWAY, headers={"Authorization": bearer_token, "captcha-token": captcha_token}, json=verify_email_body)
    print(res.json())
    """


main()
