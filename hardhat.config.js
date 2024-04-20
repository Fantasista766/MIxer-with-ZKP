require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();
const { API_URL, PRIVATE_KEY, API_KEY } = process.env;
/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.24",
  networks: {
    sepolia: {
      url: API_URL,
      accounts: [PRIVATE_KEY]
    }
  },
  etherscan: {
    apiKey: {
      sepolia: API_KEY
    }
  }
};