// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./IDigitalRub.sol";

contract DigitalRub is IDigitalRub {
    uint totalTokens;
    address owner = 0x7847150AB80cB9fD02f56e616E3912a2d8119799;
    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowances;
    string _name = "digitalRub";
    string _symbol = "dRub";

    constructor() {
        mint(address(this), 500);
    }

    modifier enoughTokens(address _from, uint _amount) {
        require(balanceOf(_from) >= _amount, "not enough tokens!");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not an owner!");
        _;
    }

    function name() external view returns (string memory) {
        return _name;
    }

    function symbol() external view returns (string memory) {
        return _symbol;
    }

    function decimals() external pure returns (uint) {
        return 18; // 1 token = 1 wei
    }

    function totalSupply() external view returns (uint) {
        return totalTokens;
    }

    function balanceOf(address _account) public view returns (uint) {
        return balances[_account];
    }

    function transfer(
        address _to,
        uint _amount
    ) external enoughTokens(msg.sender, _amount) {
        balances[msg.sender] -= _amount;
        balances[_to] += _amount;
        emit Transfer(msg.sender, _to, _amount);
    }

    function mint(address _account, uint _amount) public onlyOwner {
        balances[_account] += _amount;
        totalTokens += _amount;
        emit Transfer(address(0), _account, _amount);
    }

    function burn(
        address _account,
        uint _amount
    ) public onlyOwner enoughTokens(_account, _amount) {
        balances[_account] -= _amount;
        totalTokens -= _amount;
    }

    function allowance(
        address _owner,
        address _spender
    ) public view returns (uint) {
        return allowances[_owner][_spender];
    }

    function approve(address _spender, uint _amount) public {
        allowances[msg.sender][_spender] = _amount;
        emit Approve(msg.sender, _spender, _amount);
    }

    function transferFrom(
        address _from,
        address _to,
        uint _amount
    ) public enoughTokens(_from, _amount) {
        require(allowances[_from][msg.sender] >= _amount, "check allowance!");
        allowances[_from][msg.sender] -= _amount;

        balances[_from] -= _amount;
        balances[_to] += _amount;
        emit Transfer(_from, _to, _amount);
    }
}
