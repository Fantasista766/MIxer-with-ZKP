// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

interface IDigitalRub {
    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function decimals() external pure returns (uint);

    function totalSupply() external view returns (uint);

    function balanceOf(address _account) external view returns (uint);

    function transfer(address _to, uint _amount) external;

    function allowance(
        address _owner,
        address _spender
    ) external view returns (uint);

    function approve(address _spender, uint _amount) external;

    function transferFrom(address _from, address _to, uint _amount) external;

    event Transfer(address indexed from, address indexed to, uint amount);
    event Approve(address indexed owner, address indexed spender, uint amount);
}
