// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./DigitalRub.sol";

interface IVerifier {
    function verifyProof(
        uint[2] calldata _pA,
        uint[2][2] calldata _pB,
        uint[2] calldata _pC,
        uint[1] calldata _pubSignals
    ) external view returns (bool);
}

contract Mixer {
    mapping(address => uint) balances;
    mapping(address => bool) commitments;
    bytes32 valueToProof;
    uint mixerTotalAmount;
    uint randNonce;
    address[] fakeAddresses;

    DigitalRub public dRub;
    IVerifier public verifier;

    event Deposit(address indexed sender, uint indexed amount);
    event Withdraw(address indexed sender);
    event Mix();

    constructor(address tokenAddress) {
        dRub = DigitalRub(tokenAddress);
    }

    receive() external payable {}

    function currentDeposit(address account) external view returns (uint) {
        return balances[account];
    }

    function randMod(uint _modulus) internal returns (uint) {
        randNonce++;
        return
            uint(
                keccak256(abi.encode(block.timestamp, msg.sender, randNonce))
            ) % _modulus;
    }

    // проверям отсутствие двойного депонирования
    // в качестве секрета храним значение, знание которого должен доказать получатель
    // если депонирование с нескольких адресов, то это значение должно оставаться таким же
    // изменяем соответствующие балансы
    function deposit(uint _amount, bytes32 _valueToProof) public {
        require(!commitments[msg.sender], "double commitment");
        if (valueToProof == 0x0) {
            valueToProof = _valueToProof;
        }

        require(
            valueToProof == _valueToProof,
            "you've provided wrong value to proof!"
        );
        commitments[msg.sender] = true;

        dRub.transferFrom(msg.sender, address(this), _amount);
        balances[msg.sender] += _amount;
        mixerTotalAmount += _amount;
        emit Deposit(msg.sender, _amount);
    }

    // отправитель средств добавляет контракт для проверки доказательства
    function addVerifier(address verifierAddress) public {
        require(
            commitments[msg.sender],
            "msg sender is not in senders or verifier has been already added"
        );
        verifier = IVerifier(verifierAddress);
    }

    // сначала закидываем на все псевдо адреса по одинаковому количеству монет
    // затем с каждого псевдо адреса отправляем случайное количество на случайный псевдо адрес (или в случае совпадения не отправляем)
    // потом отправляем средства на адрес получателя
    function mix(address[] memory _addresses) public {
        require(
            commitments[msg.sender],
            "msg sender is not in senders or has already mixed tokens"
        );
        require(
            balances[msg.sender] ==
                (balances[msg.sender] / _addresses.length) * _addresses.length,
            "mixing adresses quantity have to divide your tokens quantity!"
        );

        uint amount_per_address = balances[msg.sender] / _addresses.length;
        for (uint i = 0; i < _addresses.length; i++) {
            dRub.transfer(_addresses[i], amount_per_address);
            balances[_addresses[i]] += amount_per_address;
            balances[msg.sender] -= amount_per_address;
        }

        for (uint i = 0; i < _addresses.length; i++) {
            uint j = randMod(_addresses.length);
            uint partial_amount_per_address = randMod(amount_per_address);
            if (i != j) {
                dRub.transferFrom(
                    _addresses[i],
                    _addresses[j],
                    partial_amount_per_address
                );
                balances[_addresses[j]] += partial_amount_per_address;
                balances[_addresses[i]] -= partial_amount_per_address;
            }
        }

        commitments[msg.sender] = false;
        fakeAddresses = _addresses;
        emit Mix();
    }

    // при снятии средств получатель отправляет доказательство знания значения отправителя
    // здесь проверяется, что микширование проведено и доказательство предоставлено
    function withdraw(
        uint[2] calldata _pA,
        uint[2][2] calldata _pB,
        uint[2] calldata _pC,
        uint[1] calldata _pubSignals
    ) public {
        require(fakeAddresses.length > 0, "tokens haven't been mixed yet!");
        require(
            verifier.verifyProof(_pA, _pB, _pC, _pubSignals),
            "proof has not been accepted!"
        );

        for (uint i = 0; i < fakeAddresses.length; i++) {
            if (balances[fakeAddresses[i]] != 0) {
                dRub.transferFrom(
                    fakeAddresses[i],
                    msg.sender,
                    balances[fakeAddresses[i]]
                );
                mixerTotalAmount -= balances[fakeAddresses[i]];
                balances[fakeAddresses[i]] = 0;
            }
        }

        valueToProof = 0x0;
        delete fakeAddresses;

        emit Withdraw(msg.sender);
    }
}
