async function main() {
    const [deployer] = await ethers.getSigners();

    console.log("Deployer address:", deployer.address);

    console.log("Account balance:", (await deployer.provider.getBalance(deployer.address)).toString());

    const DigitalRub = await ethers.getContractFactory("DigitalRub");
    const digitalRub = await DigitalRub.deploy();
    await digitalRub.waitForDeployment();
    const digitalRubAddress = await digitalRub.getAddress();
    console.log("Token address:", digitalRubAddress);

    const Mixer = await ethers.getContractFactory("Mixer");
    const mixer = await Mixer.deploy(digitalRubAddress);
    await mixer.waitForDeployment();
    const mixerAddress = await mixer.getAddress();
    console.log("Mixer address:", mixerAddress);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });