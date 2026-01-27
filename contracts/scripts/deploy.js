const hre = require("hardhat");

async function main() {
  const HallucinationTracker = await hre.ethers.getContractFactory("HallucinationTracker");
  const tracker = await HallucinationTracker.deploy();
  await tracker.deployed();
  console.log("Contract deployed to:", tracker.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});