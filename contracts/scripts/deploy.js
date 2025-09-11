const fs = require("fs");
const path = require("path");

async function main() {
  const SnippetRegistry = await ethers.getContractFactory("SnippetRegistry");
  const registry = await SnippetRegistry.deploy();
  await registry.deployed();

  console.log("SnippetRegistry deployed to:", registry.address);

  // Save to shared volume
  const outputDir = path.resolve(__dirname, "../deployment");
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }

  fs.writeFileSync(
    path.join(outputDir, "deployed.json"),
    JSON.stringify({ address: registry.address }, null, 2)
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
