async function main() {
    const [deployer] = await ethers.getSigners();

    console.log("Deployer address:", deployer.address);

    console.log("Account balance:", (await deployer.provider.getBalance(deployer.address)).toString());

    const Verifier = await ethers.getContractFactory("Groth16Verifier");
    const verifier = await Verifier.deploy();
    await verifier.waitForDeployment();
    const verifierAddress = await verifier.getAddress();
    console.log("Verifier address:", verifierAddress);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });