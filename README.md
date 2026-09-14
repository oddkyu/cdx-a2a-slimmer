# 🚀 CDX A2A Slimmer (Cantor Diagonal eXpress)

[![PyPI Version](https://img.shields.io/badge/PyPI-v1.0.0-blue.svg)](https://pypi.org/project/cdx-a2a-slimmer/)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-cdxno1%2Fcdx--a2a--sidecar-2496ED.svg)](https://hub.docker.com/r/cdxno1/cdx-a2a-sidecar)
[![Python Support](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-success.svg)](https://pypi.org/project/cdx-a2a-slimmer/)
[![License](https://img.shields.io/badge/License-Commercial%20EULA-darkred.svg)](./EULA.md)
[![Patent](https://img.shields.io/badge/Patent-Pending%20(KR%2010--2026--0172394)-gold.svg)](./EULA.md)

> **"Cache-Preserving Zero-Loss Token Slimming, The New Standard for Multi-Agent AI"**  
> Reduce your OpenAI, Anthropic, and open LLM multi-agent communication tokens by **20% ~ 31.55%** with **zero code refactoring** and **0.08ms ultra-low latency**.

---

## ⚡ 1-Minute Quickstart

### Path 1: Docker Sidecar (macOS Apple Silicon M1~M4 & Linux)
Run the official multi-arch hardened sidecar proxy on port 8080:

```bash
docker run -d \
  --name cdx-a2a-sidecar \
  -p 8080:8080 \
  -e TARGET_UPSTREAM="https://api.openai.com" \
  cdxno1/cdx-a2a-sidecar:latest
```

Or using Docker Compose:
```bash
docker-compose up -d
```

### Path 2: Python SDK (Windows & Python Environments)
Install the sealed C-binary package from PyPI:

```bash
pip install cdx-a2a-slimmer
```

---

## 🔌 Client Integration (Change 1 Line)

Redirect your existing OpenAI or AI framework client to the local CDX proxy:

```python
from openai import OpenAI

# Simply redirect base_url to the CDX sidecar proxy!
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="YOUR_OPENAI_API_KEY"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Analyze system performance."}],
    tools=[...]  # Large JSON schemas and agent histories are pruned automatically!
)
```

---

## 📊 Performance Benchmarks

| Metric | Raw Multi-Agent Traffic | With CDX A2A Slimmer | Improvement |
| :--- | :---: | :---: | :---: |
| **Tool JSON Schema Tokens** | 4,120 tokens | **3,296 tokens** | **-20.0%** (Free Tier) |
| **Multi-Agent Message History** | 8,450 tokens | **5,784 tokens** | **-31.55%** (Pro Tier) |
| **KV Cache Prefix Alignment** | Fragmented | **100.0% Normalized** | **Max Cache Discount** |
| **Proxy Processing Latency** | — | **< 0.08 ms** | **Near Zero Overhead** |
| **Agent Tool Execution Accuracy (Pass@1)**| 100.0% | **100.0%** | **Zero Intelligence Loss** |

---

## 🛡️ Enterprise Privacy & Air-Gapped Security

* **100% On-Premises Execution:** All payload normalization and pruning occur strictly in local memory. No payload data is ever transmitted to external third-party servers.
* **Non-Root Sandboxed Execution:** Docker containers run under UID 10001 (`cdxuser`).
* **Zero Plain-Text Python Code:** All distributed runtimes are protected by compiled C-extensions (`.pyd`) and encrypted bytecode runtimes (`.pyc`).

---

## 📜 Intellectual Property & Patent Protection

This software is protected by trade secret law and pending patent applications:
* **Korean Patent Application No. 10-2026-0172394**
* **Korean Patent Application No. 10-2026-0175561**

Reverse engineering, decompilation, disassembly, or extraction of internal AST heuristics, codebooks, or algorithms is strictly prohibited under the [End-User License Agreement (EULA)](./EULA.md).

---

## 🌐 Links & Resources

* **Official Developer Portal:** [https://cdxengine.com](https://cdxengine.com)
* **PyPI Package:** [https://pypi.org/project/cdx-a2a-slimmer/](https://pypi.org/project/cdx-a2a-slimmer/)
* **Docker Hub Repository:** [https://hub.docker.com/r/cdxno1/cdx-a2a-sidecar](https://hub.docker.com/r/cdxno1/cdx-a2a-sidecar)
* **License Agreement:** [EULA.md](./EULA.md) | [한국어 약관](./EULA.ko.md)
* **Inquiries:** `contact@cdxengine.com`
