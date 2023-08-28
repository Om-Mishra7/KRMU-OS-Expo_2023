import json
from time import sleep
from solcx import install_solc, compile_standard
from web3 import Web3
from pymongo import MongoClient
from web3.middleware import geth_poa_middleware


install_solc("0.8.0")



uri = "mongodb+srv://contact:jVJ3cGZmKC4bfqDe@cluster0.dhcehpa.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client.get_database("certsecure")

records = db.certificates

    

# Connecting to the blockchain
w3 = Web3(
    Web3.HTTPProvider(
        "https://polygon-mumbai.g.alchemy.com/v2/mdeLrZjWjJRKM0wbyWNQmAesbyH0KyMC"
    )
)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

chain_id = 80001
certsecure_address = "0x8AC1179c9116249eb123f8286E40Dd6D55190EA4"
certsecure_private_key = (
    "c65104e2ed88d99af57c5b71ebc1a4ca7e15ccab0a050b237c90942cc5248b9d"
)


def generateCertificate(
    _CertificateID,
    _StudentName,
    _StudentCGP,
    _StudentProfilePictureUrl,
    _CertificateTitle,
    _IssuingAuthority,
    _IssuingDate,
):
    with open("app/contracts/Certificate.sol", "r") as file:
        contract_file = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Certificate.sol": {"content": contract_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.0",
    )

    with open("compiled_contract.json", "w") as file:
        json.dump(compiled_sol, file)

    with open("compiled_contract.json", "r") as file:
        compiled_sol = json.load(file)

    bytecode = compiled_sol["contracts"]["Certificate.sol"]["Certificate"]["evm"][
        "bytecode"
    ]["object"]

    abi = compiled_sol["contracts"]["Certificate.sol"]["Certificate"]["abi"]

    with open("abi_code.json", "w") as file:
        json.dump(abi, file)

    # Deploying smart contract

    Certificate = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Building the contract

    transaction = Certificate.constructor().build_transaction(
        {
            "chainId": chain_id,
            "from": certsecure_address,
            "nonce": w3.eth.get_transaction_count(certsecure_address),
            "gas": 1728712,
        }
    )

    signed_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=certsecure_private_key
    )

    txn_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    certificate = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

    certificateBuild = certificate.functions.generateCertificateBody(
        _CertificateID,
        _StudentName,
        _StudentCGP,
        _StudentProfilePictureUrl,
        _CertificateTitle,
        _IssuingAuthority,
        _IssuingDate,
    ).build_transaction(
        {
            "chainId": chain_id,
            "from": certsecure_address,
            "nonce": w3.eth.get_transaction_count(certsecure_address),
        }
    )

    signed_generateCertificateBody = w3.eth.account.sign_transaction(
        certificateBuild, private_key=certsecure_private_key
    )
    generateCertificateBody_hash = w3.eth.send_raw_transaction(
        signed_generateCertificateBody.rawTransaction
    )
    generateCertificateBody_receipt = w3.eth.wait_for_transaction_receipt(
        generateCertificateBody_hash
    )

    data = viewCertificate(txn_receipt.contractAddress)

    if data[0] == _CertificateID:
        records.update_one(
            {"_id": _CertificateID},
            {"$set": {"status": "generated", "address": txn_receipt.contractAddress}},
        )

    


def viewCertificate(address):
    with open("abi_code.json", "r") as abi_file:
        abi = abi_file.read()
    try:
        certificate = w3.eth.contract(address=address, abi=abi)
        viewCertificateBody = certificate.functions.getCertificateBody().call()
        return list(viewCertificateBody)
    except:
        return None



def process_data():
    data = list(records.find({"status": "pending"}))
    if data is not None and len(data) > 0:
        for i in data:
            records.update_one(
                {"_id": i["_id"]},
                {"$set": {"status": "generating"}},
            )
            generateCertificate(
                i["_id"],
                i["student_name"],
                i["student_cgp"],
                i["student_profile_picture_url"],
                i["certificate_title"],
                i["issuing_authority"],
                i["issuing_date"],
            )
    else:
        print("No pending certificates")
        return "No pending certificates"