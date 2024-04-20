from config import create_wallets


def main():
    with open('test_users.txt', 'w') as outfile:
        for acc in create_wallets(2):
            outfile.write(f'{acc.address} {acc.privateKey.hex()}\n')


if __name__ == '__main__':
    main()
