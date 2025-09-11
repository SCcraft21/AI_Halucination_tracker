Hallucination Tracker - Local demo (MVP)
=======================================

This archive contains a local demo of the Hallucination Tracker (MVP).
It includes:
- Hardhat local node (contracts/)
- FastAPI backend (backend/)
- Next.js frontend (frontend/)
- docker-compose.yml to bring up all services

How to run (quick):
1. Unzip and cd into the project root.
2. Run: docker-compose up --build -d
3. Deploy contracts to the Hardhat node (in separate terminal):
   docker exec -it hardhat-node npx hardhat run scripts/deploy.js --network localhost
   This will write contracts/deployment/deployed.json with the address.
4. Restart backend so it can read the deployed.json:
   docker-compose restart backend
5. Visit frontend: http://localhost:3000
   Backend docs: http://localhost:8000/docs

Notes:
- This is an MVP for local testing. IPFS uploads are mocked unless WEB3_STORAGE_TOKEN is set in backend env.
- For production, implement secure signing for on-chain transactions and sandboxed execution for runtime checks.
