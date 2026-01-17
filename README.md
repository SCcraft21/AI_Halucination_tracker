This README is designed to be high-impact, explaining the **why** as much as the **how**. It positions your project as a sophisticated bridge between decentralized infrastructure and AI reliability.

---

# DeHallucinate-Web3: Decentralized AI Hallucination Tracker

**DeHallucinate-Web3** is a decentralized protocol designed to track, verify, and log Large Language Model (LLM) hallucinations on-chain. By leveraging the **Bombay Testnet**, this project provides an immutable audit trail for AI behavior, ensuring that factual inconsistencies are recorded in a transparent and tamper-proof manner.

---

## 📖 Table of Contents

* [The Problem](https://www.google.com/search?q=%23the-problem)
* [Our Solution](https://www.google.com/search?q=%23our-solution)
* [System Architecture](https://www.google.com/search?q=%23system-architecture)
* [Technical Stack](https://www.google.com/search?q=%23technical-stack)
* [Smart Contract Details](https://www.google.com/search?q=%23smart-contract-details)
* [Getting Started](https://www.google.com/search?q=%23getting-started)
* [Mathematical Approach](https://www.google.com/search?q=%23mathematical-approach)

---

## 🚩 The Problem

As Generative AI becomes integrated into critical infrastructure, "hallucinations"—instances where LLMs provide confident but false information—pose a systemic risk. Currently, tracking these errors happens in centralized silos, making it possible for providers to obscure or delete logs of model failure.

## 💡 Our Solution

DeHallucinate-Web3 decentralizes the "Truth Layer" of AI. It uses a hybrid approach:

1. **AI Detection:** Analyzes LLM outputs using Natural Language Inference (NLI).
2. **Web3 Logging:** Hashes the evidence and truth-score, committing it to the **Bombay Testnet**.
3. **Immutability:** Once a hallucination is logged, it serves as a permanent public record of that model's reliability at a specific point in time.

---

## 🏗 System Architecture

The project operates through a three-tier architecture:

1. **Verification Layer (AI):** A Python-based backend that receives LLM output, retrieves reference data (RAG), and calculates a "Groundedness Score."
2. **Blockchain Layer (Web3):** A Solidity smart contract that records the model ID, the prompt hash, and the hallucination report.
3. **Interface Layer (DApp):** A Next.js frontend where users can view the "Wall of Hallucinations" and submit new samples for verification.

---

## 🛠 Technical Stack

| Component | Technology |
| --- | --- |
| **Blockchain** | Solidity, Hardhat, Ethers.js |
| **Network** | Polygon Bombay Testnet |
| **AI/ML** | Python, HuggingFace Transformers (DeBERTa-v3), LangChain |
| **Frontend** | Next.js, Tailwind CSS, RainbowKit |
| **Storage** | IPFS (via Pinata) for detailed report metadata |

---

## 📜 Smart Contract Details

The core logic is deployed on the **Bombay Testnet**.

* **Contract Name:** `HallucinationRegistry.sol`
* **Key Functions:**
* `logHallucination()`: Stores the hash of the prompt and the generated response along with the truth score.
* `getModelReputation()`: Aggregates historical data to provide a "Trust Score" for specific AI models.



> **Note:** Ensure your wallet is connected to the Bombay Testnet and has sufficient MATIC from the faucet before attempting to write to the contract.

---

## 🚀 Getting Started

### Prerequisites

* Node.js (v18+)
* Python 3.9+
* A MetaMask wallet with Bombay Testnet MATIC.

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/dehallucinate-web3.git
cd dehallucinate-web3

```


2. **Install Dependencies:**
```bash
npm install
pip install -r requirements.txt

```


3. **Environment Variables:**
Create a `.env` file in the root directory:
```env
PRIVATE_KEY=your_private_key
BOMBAY_RPC_URL=your_rpc_url
HF_API_TOKEN=your_huggingface_token

```


4. **Deploy Smart Contract:**
```bash
npx hardhat run scripts/deploy.js --network bombay

```



---

## 🧪 Mathematical Approach

We calculate the **Hallucination Index ()** based on the probability of entailment () versus contradiction () derived from the NLI model:

Where:

*  is the probability that the AI output contradicts the reference text.
*  is the probability of entailment.
*  is a small constant to prevent division by zero.

A higher  indicates a higher likelihood of hallucination, which is then flagged on-chain.

---

## 🗺 Roadmap

* [ ] Integration with Chainlink Oracles for automated off-chain verification.
* [ ] DAO governance for community-led truth verification.
* [ ] Support for multi-modal hallucinations (Images/Video).

---

**Disclaimer:** *This project is currently in Alpha and is running on a testnet. Data is for research and demonstration purposes only.*
