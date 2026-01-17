This is a top-tier, research-grade README designed for a serious GitHub repository. It uses academic language, mathematical formulation, and integrated **Mermaid.js diagrams** (which render automatically on GitHub) to explain the complex architecture.

---

# DeHallucinate Protocol: A Decentralized Oracle for Immutable LLM Verification

## 1. Abstract

The proliferation of Large Language Models (LLMs) in critical decision-making pipelines is hampered by the phenomenon of "hallucinations"—the generation of confident but factually incorrect outputs. Current evaluation methodologies are predominantly centralized and ephemeral, lacking a transparent audit trail. This project introduces the **DeHallucinate Protocol**, a decentralized architecture that bridges Natural Language Inference (NLI) with Distributed Ledger Technology (DLT). By utilizing the **Polygon Bombay Testnet** as an immutable commitment layer, we establish a trustless mechanism for logging, verifying, and auditing AI factual inconsistencies, thereby addressing the "accountability gap" in generative AI.

---

## 2. Theoretical Framework

This protocol addresses a fundamental trilemma in deploying autonomous AI agents: balancing **Performance**, **Privacy**, and **Verifiability**.

In standard centralized architectures, the entity controlling the model also controls the logs of its failures. This creates a moral hazard where systemic issues can be obscured. Our framework shifts the verification paradigm from "trusting the provider" to "trusting the protocol" by leveraging two key pillars:

1. **Cryptographic Immutability:** Using blockchain state to ensure that once an AI error is detected, its record cannot be retroactively altered.
2. **Semantic Verification:** Utilizing transformer-based NLI models as objective judges of textual entailment against verified knowledge bases (Retrieval-Augmented Generation).

---

## 3. System Architecture

The architecture operates as a hybrid on-chain/off-chain system, designed to optimize for both computational intensity (AI inference) and transaction finality (blockchain logging).

### 3.1 High-Level Data Flow

The following diagram illustrates the lifecycle of a prompt, from user submission to immutable on-chain settlement.

```mermaid
graph TD
    User[End User / Client] -->|1. Submit Prompt| DApp[Next.js DApp Interface]
    DApp -->|2. Forward Request| LLM[Target LLM API e.g., GPT-4]
    LLM -->|3. Generate Response| DApp
    DApp -->|4. Submit for Verification| Verifier[Off-Chain Verification Engine (Python)]
    
    subgraph "Verification Layer (Off-Chain)"
    Verifier -->|4a. Retrieve Context (RAG)| KnowledgeBase[(Vector DB / Trusted Source)]
    KnowledgeBase -->|4b. Return Evidence| Verifier
    Verifier -->|4c. NLI Inference| NLIModel[DeBERTa NLI Model]
    NLIModel -->|4d. Compute Score| Verifier
    end
    
    Verifier -->|5. Return Groundedness Score + Proof| DApp
    DApp -->|6. Commit Hash to Chain if Hallucinated| SmartContract[Registry Contract (Bombay Testnet)]
    SmartContract --x|7. Immutable Log Created| Blockchain[(Polygon Ledger)]
    
    style SmartContract fill:#8247e5,stroke:#fff,color:#fff
    style Blockchain fill:#8247e5,stroke:#fff,color:#fff
    style NLIModel fill:#16a34a,stroke:#fff,color:#fff

```

---

## 4. Mathematical Methodology

To rigorously quantify the concept of a "hallucination," we employ a probabilistic approach based on Natural Language Inference.

Given an LLM-generated claim  and a retrieved evidentiary premise , an NLI model computes a softmax probability distribution over three classes: Entailment (), Neutral (), and Contradiction ().

We define the **Groundedness Coefficient ()** as the normalized ratio of entailment versus contradiction, adjusting for uncertainty:

Where:

*  is a tunable hyperparameter (currently set to ) to penalize ambiguous (Neutral) relationships.
* A  score approaching 1.0 indicates high factual consistency.
* A  score approaching 0.0 indicates a high probability of hallucination.

A threshold  is utilized. If , the protocol flags the interaction and initiates an on-chain commitment transaction.

---

## 5. Technical Implementation

### 5.1 The Smart Contract (Bombay Testnet)

The core registry is deployed on Polygon's Bombay Testnet for high-throughput testing. The contract utilizes `bytes32` hashing for gas optimization.

* **Contract Address:** `[Insert Your Contract Address Here]` (Verified on Polygonscan)
* **Key Struct:**
```solidity
struct HallucinationReport {
    bytes32 contentHash; // keccak256(abi.encodePacked(prompt, response));
    uint16 groundednessScore; // Scaled Gc (e.g., 450 for 0.45)
    string modelId; // e.g., "llama-3-70b"
    uint256 timestamp;
    string ipfsProofCID; // Off-chain storage of detailed logs
}

```



### 5.2 The Verification Engine

Implemented in Python using Hugging Face Transformers and LangChain. It utilizes a cross-encoder model optimized for NLI tasks (e.g., `cross-encoder/nli-deberta-v3-large`) to maximize classification accuracy over short text pairs.

---

## 6. Installation and Replication

Prerequisites: Node.js v18+, Python 3.10+, and a Metamask wallet configured for Bombay Testnet.

### 6.1 Clone and Setup

```bash
git clone https://github.com/yourusername/dehallucinate-protocol.git
cd dehallucinate-protocol

# Install Javascript dependencies (Frontend & Contracts)
npm install

# Install Python dependencies (Verification Engine)
pip install -r requirements.txt

```

### 6.2 Environment Configuration

Create a `.env.local` file in the root directory:

```bash
# Blockchain
PRIVATE_KEY=your_testnet_private_key
BOMBAY_RPC_URL=https://rpc-mumbai.maticvigil.com/

# AI & Storage
HUGGINGFACE_API_KEY=your_hf_key
PINATA_JWT=your_ipfs_key

```

### 6.3 Run the Development Stack

```bash
# Terminal 1: Start the local verification API
python backend/main.py

# Terminal 2: Start the Next.js frontend
npm run dev

```

---

## 7. Roadmap and Future Work

This project represents the initial phase of a broader decentralized AI auditing framework.

* **Phase 2: Decentralized Verifier Network (DVN).** Transitioning from a single verification engine to a network of staked nodes performing consensus-based NLI checks using Chainlink Functions.
* **Phase 3: Zero-Knowledge Integration.** Implementing zk-SNARKs to prove that a hallucination occurred without revealing the underlying sensitive prompt data publicly on-chain.
* **Phase 4: Mainnet Deployment.** Migration to Polygon zkEVM for production readiness.

---

## 8. References

1. Ji, Z., et al. (2023). "Survey of Hallucination in Natural Language Generation." *ACM Computing Surveys*.
2. Nakamoto, S. (2008). "Bitcoin: A Peer-to-Peer Electronic Cash System." (Foundational concept of immutable logging).
3. Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS*.

---

**Author:** [Your Name]
**Contact:** [Your Email or LinkedIn Profile]
**Citation:** Please cite this repository if used in academic or commercial research.
