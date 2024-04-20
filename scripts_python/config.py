import json
import os
from dotenv import load_dotenv
from web3 import Web3


'''config information'''
owner_private_key_dir = os.path.dirname(os.getcwd()) + r'\.env'
load_dotenv(owner_private_key_dir)

# Create the node connection
sepolia_url = os.environ.get('API_URL')
w3 = Web3(Web3.HTTPProvider(sepolia_url))
sepolia_chain_id = w3.eth.chain_id

token_address = '0xe6a3B4E20b4bb4216DEB2834A97Ede20F82EeE25'
mixer_address = '0x25bB1Bf9b59040bfde2B4eB4eC03dffE2C041cF9'
verifier_address = '0x979f3be8d44E32B56909DB16614F07CE6C4b5291'

owner_private_key = os.environ.get('PRIVATE_KEY')
owner = w3.eth.account.from_key(private_key=owner_private_key)

abi_dir = os.path.dirname(os.getcwd()) + r'\artifacts\contracts\DigitalRub.sol'
abi_data = json.loads(open(abi_dir + '\\DigitalRub.json').read())['abi']
token_contract = w3.eth.contract(address=token_address, abi=abi_data)  # здесь всё норм
token_pool = token_contract.functions

abi_dir = os.path.dirname(os.getcwd()) + r'\artifacts\contracts\Mixer.sol'
abi_data = json.loads(open(abi_dir + '\\Mixer.json').read())['abi']
mixer_contract = w3.eth.contract(address=mixer_address, abi=abi_data)  # здесь всё норм
mixer_pool = mixer_contract.functions

# на всякий случай, скорее всего не понадобится
# abi_dir = os.path.dirname(os.getcwd()) + r'\artifacts\contracts\verifier.sol'
# abi_data = json.loads(open(abi_dir + '\\verifier.json').read())['abi']
# verifier_contract = w3.eth.contract(address=verifier_address, abi=abi_data)  # здесь всё норм
# verifier_pool = verifier_contract.functions

# loading test users data
with open('test_users.txt', 'r') as infile:
    users_data = infile.readlines()
users = [user.split() for user in users_data]  # users[i][0] for address, users[i][1] for private key

# loading fake addresses
with open('fake_addresses.txt', 'r') as infile:
    users_data = infile.readlines()
fake_users = [user.split() for user in users_data]

# define sender and recipient
sender = users[0]
recipient = users[1]

# sender sends a value to proof
value_to_proof = '85df8945419d2b5038f7ac83ec1ec6b8267c40fdb3b1e56ff62f6676eb855e70'
secret = bytes.fromhex(value_to_proof)

# loading proof and preparing it for interaction with mixer
with open('proof.txt', 'r') as infile:
    proof_data = infile.read()
proof_data = json.loads(proof_data)
_pA, _pB, _pC, _pubSignals = proof_data
_pA = [int(i, 16) for i in _pA]
_pB = [[int(j, 16) for j in i] for i in _pB]
_pC = [int(i, 16) for i in _pC]
_pubSignals = [int(i, 16) for i in _pubSignals]


def create_wallets(quantity):
    return [w3.eth.account.create() for _ in range(quantity)]


def get_balances(pre_string=''):
    print(pre_string)
    print('Total token amount:', token_pool.totalSupply().call())
    for i, user in enumerate(users, 1):
        user_address, user_private_key = user
        print(f'User {i} balance:', token_pool.balanceOf(user_address).call())
    print(f'Mixer balance:', token_pool.balanceOf(mixer_address).call())
    print()


def get_current_deposit(user, user_name):
    user_address, user_private_key = user
    print(f'{user_name} deposit:', str(mixer_pool.current_deposit(user_address).call()))


def check_allowance(user, user_name):
    user_address, user_private_key = user
    print(f'{user_name} allowance to mixer:', str(token_pool.allowance(user_address, mixer_address).call()))


def check_balance(user, user_name):
    user_address, user_private_key = user
    print(f'{user_name} balance:', str(token_pool.balanceOf(user_address).call()))


def mint_tokens_to_users():
    print('Minting...')
    for i, user in enumerate(users, 1):
        user_address, _ = user
        transaction = token_pool.mint(user_address, 250).build_transaction({
            'from': owner.address,
            'nonce': w3.eth.get_transaction_count(owner.address)
        })
        signed_tx = w3.eth.account.sign_transaction(transaction, private_key=owner.key)
        send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'Transaction hash: {send_tx.hex()}')
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
        print(tx_receipt)
    print('MINT OK')


def approve(user, amount):
    print('Approving...')
    user_address, user_private_key = user
    transaction = token_pool.approve(mixer_address, amount).build_transaction({
        'from': user_address,
        'nonce': w3.eth.get_transaction_count(user_address)
    })

    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=user_private_key)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f'Transaction hash: {send_tx.hex()}')
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)
    print('APPROVE OK')


def deposit_tokens_to_mixer(user):
    print('Depositing...')
    user_address, user_private_key = user
    transaction = mixer_pool.deposit(100, secret).build_transaction({
        'from': user_address,
        'nonce': w3.eth.get_transaction_count(user_address)
    })

    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=user_private_key)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f'Transaction hash: {send_tx.hex()}')
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)
    print('DEPOSIT OK')


def add_verifier_address(user):
    print('Adding verifier address...')
    user_address, user_private_key = user
    transaction = mixer_pool.addVerifier(verifier_address).build_transaction({
        'from': user_address,
        'nonce': w3.eth.get_transaction_count(user_address)
    })

    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=user_private_key)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f'Transaction hash: {send_tx.hex()}')
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)
    print('ADDING VERIFIER OK')


def mix(user):
    print('Mixing...')
    user_address, user_private_key = user
    fake_addresses = [fake_user[0] for fake_user in fake_users]
    transaction = mixer_pool.mix(fake_addresses).build_transaction({
        'from': user_address,
        'nonce': w3.eth.get_transaction_count(user_address)
    })

    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=user_private_key)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f'Transaction hash: {send_tx.hex()}')
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)
    print('MIX OK')


def withdraw(user):
    print('Withdrawing...')
    user_address, user_private_key = user
    transaction = mixer_pool.withdraw(_pA, _pB, _pC, _pubSignals).build_transaction({
        'from': user_address,
        'nonce': w3.eth.get_transaction_count(user_address)
    })

    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=user_private_key)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)
    print('WITHDRAW OK')


def before_verifier_deploy():
    # test initial amount of token
    get_balances('Before minting:')

    # 1) Mint token to users 1 and 2
    mint_tokens_to_users()
    get_balances('After minting:')

    # 2) Sender deposits tokens to mixer
    approve(sender, 100)
    check_allowance(sender, 'Sender')
    deposit_tokens_to_mixer(sender)
    get_balances('After deposit:')
    get_current_deposit(sender, 'Sender')


def after_verifier_deploy():
    # 3) After verifier contract deployment the sender adds the contract address to mixer address
    add_verifier_address(sender)

    # 4) Mixing. The sender provides fake addresses to mixer, but first one needs to approve that mixer can transfer
    # tokens from one fake account to another to mixer
    for fake_user in fake_users:
        approve(fake_user, 50)
    for i, fake_user in enumerate(fake_users, 1):
        check_allowance(fake_user, f'Fake user {i}')

    mix(sender)
    get_balances('After mixing:')
    get_current_deposit(sender, 'Sender')
    for i, fake_user in enumerate(fake_users, 1):
        check_balance(fake_user, f'Fake user {i}')

    # 5) The recipient withdraws his tokens
    withdraw(recipient)
    get_balances('After withdraw:')
    for i, fake_user in enumerate(fake_users, 1):
        check_balance(fake_user, f'Fake user {i}')


def main():
    c = input("Choose the scenario:\n 1 - before verifier deployment, 2 - after: ")
    if c == '1':
        before_verifier_deploy()
    elif c == '2':
        after_verifier_deploy()


if __name__ == '__main__':
    main()
