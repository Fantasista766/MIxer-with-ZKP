from config import create_wallets


def main():
    with open('fake_addresses.txt', 'w') as outfile:
        for acc in create_wallets(5):
            outfile.write(f'{acc.address} {acc.privateKey.hex()}\n')


if __name__ == '__main__':
    main()
