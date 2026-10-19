const hre = require("hardhat");

async function main() {
  const Trust = await hre.ethers.getContractFactory("Trust");
  const trust = await Trust.deploy();

  // FIXED LINE
  await trust.waitForDeployment();

  const address = await trust.getAddress();

  console.log("✅ Contract deployed to:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});