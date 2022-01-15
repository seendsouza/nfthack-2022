import sys
import json
import rlp
import logging
from time import sleep
from datetime import datetime, timedelta

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from web3 import Web3, exceptions
from trezorlib.client import get_default_client
from trezorlib.tools import parse_path
from trezorlib import ethereum

from axie.schemas import breeding_schema
from axie.utils import (
    get_nonce,
    load_json,
    RONIN_PROVIDER_FREE,
    AXIE_CONTRACT,
    check_balance,
    TIMEOUT_MINS,
    ImportantLogsFilter,
)
from axie.payments import PaymentsSummary, CREATOR_FEE_ADDRESS
from axie.utils import USER_AGENT
from trezor.trezor_payments import TrezorPayment
from trezor.trezor_utils import CustomUI


now = int(datetime.now().timestamp())
log_file = f"logs/results_{now}.log"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.addFilter(ImportantLogsFilter())
logger.addHandler(file_handler)


class TrezorBreed:
    def __init__(self, sire_axie, matron_axie, address, client, bip_path):
        self.w3 = Web3(
            Web3.HTTPProvider(
                RONIN_PROVIDER_FREE,
                request_kwargs={
                    "headers": {
                        "content-type": "application/json",
                        "user-agent": USER_AGENT,
                    }
                },
            )
        )
        self.sire_axie = sire_axie
        self.matron_axie = matron_axie
        self.address = address.replace("ronin:", "0x")
        self.client = client
        self.bip_path = parse_path(bip_path)
        self.gwei = self.w3.toWei("0", "gwei")
        self.gas = 250000

    def execute(self):
        # Prepare transaction
        with open("axie/axie_abi.json") as f:
            axie_abi = json.load(f)
        axie_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(AXIE_CONTRACT), abi=axie_abi
        )
        # Get Nonce
        nonce = get_nonce(self.address)
        # Build transaction
        breed_tx = axie_contract.functions.breedAxies(
            self.sire_axie, self.matron_axie
        ).buildTransaction(
            {
                "chainId": 2020,
                "gas": self.gas,
                "gasPrice": self.w3.toWei("0", "gwei"),
                "nonce": nonce,
            }
        )
        data = self.w3.toBytes(hexstr=breed_tx["data"])
        to = self.w3.toBytes(hexstr=AXIE_CONTRACT)
        sig = ethereum.sign_tx(
            self.client,
            n=self.bip_path,
            nonce=nonce,
            gas_price=self.gwei,
            gas_limit=self.gas,
            to=AXIE_CONTRACT,
            value=0,
            data=data,
            chain_id=2020,
        )
        logging.info(f"Important: Debugging information {sig}")
        l_sig = list(sig)
        l_sig[1] = l_sig[1].lstrip(b"\x00")
        l_sig[2] = l_sig[2].lstrip(b"\x00")
        sig = tuple(l_sig)
        transaction = rlp.encode((nonce, self.gwei, self.gas, to, 0, data) + sig)
        # Send raw transaction
        self.w3.eth.send_raw_transaction(transaction)
        # get transaction hash
        hash = self.w3.toHex(self.w3.keccak(transaction))
        # Wait for transaction to finish or timeout
        logging.info("{self} about to start!")
        start_time = datetime.now()
        while True:
            # We will wait for max 10minutes for this tx to respond
            if datetime.now() - start_time > timedelta(minutes=TIMEOUT_MINS):
                success = False
                logging.info(f"Transaction {self}, timed out!")
                break
            try:
                recepit = self.w3.eth.get_transaction_receipt(hash)
                if recepit["status"] == 1:
                    success = True
                else:
                    success = False
                break
            except exceptions.TransactionNotFound:
                # Sleep 10s while waiting
                sleep(10)
                logging.info(
                    f"Waiting for transactions '{self}' to finish (Nonce: {nonce})..."
                )

        if success:
            logging.info(f"Important: {self} completed successfully")
        else:
            logging.info(f"Important: {self} failed")

    def __str__(self):
        return (
            f"Breeding axie {self.sire_axie} with {self.matron_axie} in account "
            f"{self.address.replace('0x', 'ronin:')}"
        )


class TrezorAxieBreedManager:
    def __init__(self, breeding_file, trezor_config, payment_account):
        self.trezor_config = load_json(trezor_config)
        self.breeding_file = load_json(breeding_file)
        self.payment_account = payment_account.lower()
        self.breeding_costs = 0

    def verify_inputs(self):
        validation_error = False
        logging.info("Validating file inputs...")
        try:
            validate(self.breeding_file, breeding_schema)
        except ValidationError as ex:
            logging.critical(
                f"Validation of breeding file failed. Error given: {ex.message}\n"
                f"For attribute in: {list(ex.path)}"
            )
            validation_error = True
        for acc in self.breeding_file:
            if acc["AccountAddress"].lower() not in self.trezor_config:
                logging.critical(
                    f"Account '{acc['AccountAddress']}' is not present in trezor config, "
                    "please re-run setup."
                )
                validation_error = True
        if self.payment_account not in self.trezor_config:
            logging.critical(
                f"Payment account '{self.payment_account}' is not present in trezor config, "
                "please re-run setup."
            )
            validation_error = True
        if validation_error:
            sys.exit()

    def calculate_cost(self):
        return self.calculate_fee_cost() + self.breeding_costs

    def calculate_breeding_cost(self):
        # TODO: We need to calculate how much will all breeding cost, pending for the future!
        return 0

    def calculate_fee_cost(self):
        number_of_breeds = len(self.breeding_file)
        if number_of_breeds <= 15:
            cost = number_of_breeds * 30
        if 15 < number_of_breeds <= 30:
            cost = (15 * 30) + ((number_of_breeds - 15) * 25)
        if 30 < number_of_breeds <= 50:
            cost = (15 * 30) + (15 * 25) + ((number_of_breeds - 30) * 20)
        if number_of_breeds > 50:
            cost = (15 * 30) + (15 * 25) + (20 * 20) + ((number_of_breeds - 50) * 15)
        return cost

    def execute(self):
        if check_balance(self.payment_account) < self.calculate_cost():
            logging.critical("Not enough SLP funds to pay for breeding and the fee")
            sys.exit()

        logging.info("About to start breeding axies")
        for bf in self.breeding_file:
            b = TrezorBreed(
                sire_axie=bf["Sire"],
                matron_axie=bf["Matron"],
                address=bf["AccountAddress"].lower(),
                client=get_default_client(
                    ui=CustomUI(
                        self.trezor_config[bf["AccountAddress"].lower()]["passphrase"]
                    )
                ),
                bip_path=self.trezor_config[bf["AccountAddress"].lower()]["bip_path"],
            )
            b.execute()
        logging.info("Done breeding axies")
        fee = self.calculate_fee_cost()
        logging.info(
            f"Time to pay the fee for breeding. For this session it is: {fee} SLP"
        )
        p = TrezorPayment(
            "Breeding Fee",
            "donation",
            get_default_client(
                ui=CustomUI(
                    passphrase=self.trezor_config[self.payment_account]["passphrase"]
                )
            ),
            parse_path(self.trezor_config[self.payment_account]["bip_path"]),
            self.payment_account,
            CREATOR_FEE_ADDRESS,
            fee,
            PaymentsSummary(),
        )
        p.execute()
