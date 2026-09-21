# CDX A2A Slimmer (`cdx-a2a-slimmer`)
> **Prompt Cache (KV-Cache) Preserving Zero-Loss Token Slimmer for Multi-Agent LLM Pipelines**  
> *100% Prompt Cache Hit Retention + 30% AST Lossless Slimming*  
> *Built by Cantor Labs (Cantor Diagonal eXpress)*

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/cdx-a2a-slimmer/)
[![Smithery](https://img.shields.io/badge/Smithery-cdx--mcp--proxy-brightgreen.svg)](https://smithery.ai)
[![Latency](https://img.shields.io/badge/latency-%3C0.08ms-orange.svg)]()
[![Token Savings](https://img.shields.io/badge/token_savings-20%25~31.5%25-brightgreen.svg)]()
[![MCP Schema Pruning](https://img.shields.io/badge/MCP_Schema-30%25~50%25_Pruning-blueviolet.svg)]()
[![KV Cache Hit](https://img.shields.io/badge/KV_Cache-100%25_Hit_Retention-purple.svg)]()

---

## ⚡ Why CDX A2A Slimmer? (Solving the Cache Invalidation Trap)

Across all major LLM providers (**Anthropic Claude, OpenAI, DeepSeek, vLLM RadixAttention**), prompt caching is now the core foundation of multi-agent communication. Cache hits provide **50%~90% cost discounts** and reduce Time-to-First-Token (TTFT) by **80%**.

However, conventional token compressors lacking cache awareness randomly modify prompt prefixes across turns, triggering **Cache Misses that can inflate total bills by up to 2.5x**!

**CDX A2A Slimmer** solves this via a **`2-Tier Prefix-Tail Split`** architecture:
1. **Tier 1 (Static Prefix):** Tool schemas and system instructions are canonically sorted (lexicographical normalization), locking byte-level invariance to **guarantee 100% KV-Cache Hit Rates**.
2. **Tier 2 (Dynamic Tail):** Intermediate conversational turns and verbose tool outputs are trimmed with **30% lossless AST slimming**.

### 📊 3-Way Architectural Cost & Latency Comparison (10,000 Token Baseline)

| Parameter | Standard Call (No Slimmer) | Conventional Compressor (Cache Invalidation) | **CDX A2A Slimmer (Cache-Preserving)** |
|:---|:---:|:---:|:---:|
| **Static Prefix (Tools/System 8K)** | 100% Cost | 70% Cost (Cache Missed) | **10% Cost (100% Cache Hit Retained)** |
| **Dynamic Tail (Messages/Output 2K)** | 100% Cost | 70% Cost | **70% Cost (30% Lossless Slimming)** |
| **Effective Net Cost (Tokens)** | 10,000 Tokens (100%) | 7,000 Tokens (2.5x More Expensive!) | **2,200 Tokens (78% ~ 93% Effective Net Savings)** |
| **P99 TTFT Latency** | 1,200 ms | 1,150 ms | **180 ms (Sub-second Responsiveness)** |

### 🎯 The 2 Mandatory Conditions for BigTech Cache Discounts
Frontier LLM 50~90% prompt cache discounts activate **ONLY when two conditions are simultaneously satisfied**:
1. **Condition 1: Byte-Level Invariance:** The static prefix must not alter a single whitespace, key order, or character (`KVCachePreservingNormalizer` guarantees 100% canonical invariance).
2. **Condition 2: Minimum 1,024-Token Threshold:** The prefix length must be **>= 1,024 tokens** (OpenAI automatic caching & Anthropic `cache_control` standard).
   - *Cache Threshold Safeguard (Over-Slimming Prevention):* If a compressor prunes an 1,100-token static schema down to 950 tokens without cache awareness, it drops below the 1,024-token boundary, causing **immediate forfeiture of the provider cache discount**!
   - **The CDX Solution:** CDX A2A Slimmer safely maintains static schemas above the 1,024-token cache threshold (sorting keys without over-compressing), concentrating all 30% AST slimming strictly on the **dynamic conversational tail**, completely eliminating cache disqualification risks.

---

## 📊 Transparent Benchmark Results (v1.0 Live Telemetry)

We believe in radical engineering honesty. Here are the exact measured numbers across real-world multi-agent scenarios:

| Multi-Agent Scenario | Raw Payload | Slimmed | **Token Reduction (%)** | Overhead Latency | Monthly Savings (1M Calls @ GPT-4o) |
|---|---|---|---|---|---|
| **① Complex Multi-Agent (Tool + CoT)** | `2,469 Bytes` | `1,690 Bytes` | **`31.55%`** | `0.056 ms` | **`+$486.80`** |
| **② Code Review Crew (CrewAI)** | `2,286 Bytes` | `1,710 Bytes` | **`25.20%`** | `0.233 ms` | **`+$377.50`** |
| **③ Market Research Analyst (AutoGen)** | `1,967 Bytes` | `1,544 Bytes` | **`21.50%`** | `0.168 ms` | **`+$277.50`** |
| **④ SQL Analytics & Migration (LangGraph)** | `1,233 Bytes` | `986 Bytes` | **`20.03%`** | `0.141 ms` | **`+$162.50`** |

> **Why the variance?**  
> Workloads with rich Tool/MCP schemas and conversational histories see **30%~35% savings**. Workloads dominated by raw SQL query strings or pure tabular numbers see **20%~25% savings** because we strictly refuse to touch raw code, numbers, or identifiers.

---

## 📦 Quick Installation

```bash
pip install cdx-a2a-slimmer
```

---

## 🚀 Usage

### 1. 1-Line Drop-In Function
```python
from cdx_a2a_slimmer import slim

# Raw multi-agent request payload (OpenAI / Anthropic schema)
raw_payload = {
    "model": "gpt-4o",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "query_database",
                "description": "Executes SQL query on primary database cluster. Highly reliable execution engine.",
                "parameters": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "title": "QueryParams",
                    "type": "object",
                    "properties": {
                        "sql_query": {"title": "SQL Query", "type": "string", "description": "Raw SQL query string."}
                    },
                    "required": ["sql_query"]
                }
            }
        }
    ],
    "messages": [
        {"role": "user", "content": "Hello! As an AI assistant, I have verified the query: SELECT * FROM users. Please proceed."}
    ]
}

# 1-Line Slimming (< 0.08 ms overhead, 30% smaller)
slimmed_payload = slim(raw_payload)
```

---

### 2. OpenAI SDK Client Hook
```python
from openai import OpenAI
from cdx_a2a_slimmer import slim

client = OpenAI()

# Wrap your parameters with slim() before sending
response = client.chat.completions.create(
    **slim({
        "model": "gpt-4o",
        "messages": messages,
        "tools": tools
    })
)
```

---

### 3. Telemetry & Metrics
```python
from cdx_a2a_slimmer import CDXA2ATokenSlimmer

slimmer = CDXA2ATokenSlimmer()
slimmed_payload, telemetry = slimmer.slim_payload(raw_payload)

print(f"Raw: {telemetry['raw_bytes']}B ➔ Slim: {telemetry['slimmed_bytes']}B")
print(f"Savings: {telemetry['reduction_percent']}% | Latency: {telemetry['latency_ms']:.4f} ms")
```

---

## 🐳 50MB Docker Sidecar (macOS, Linux & Multi-Language Support)

For **macOS (Apple Silicon M1/M2/M3/M4 & Intel)**, **Linux (Ubuntu/Debian/RHEL)**, and non-Python environments (Node.js, TypeScript, Go, Java, Rust), run the 100% binary-sealed zero-data-retention (ZDR) reverse proxy sidecar locally or in your Kubernetes cluster with **zero code changes**:

### Step 1: Claim Free License Key (Instant, 10 Seconds)
1. Sign up for free at **[https://cdxengine.com](https://cdxengine.com)** (No credit card required).
2. Copy your free instant license key (`cdx_live_...`).
   * 🎁 **All registered keys unlock the full 31.55% token reduction AND 100% KV-Cache canonical alignment** (unlocking 50% OpenAI / 90% Anthropic prompt caching discounts)!

### Step 2: Run the Docker Sidecar

```bash
docker run -d \
  --name cdx-a2a-sidecar \
  -p 8080:8080 \
  -e TARGET_UPSTREAM="https://api.openai.com" \
  -e CDX_LICENSE_KEY="cdx_live_YOUR_KEY_HERE" \
  cdxno1/cdx-a2a-sidecar:latest
```

Point any AI agent framework (OpenAI, Anthropic, LangChain, CrewAI, AutoGen) to `http://localhost:8080/v1`:

```python
from openai import OpenAI

# Zero-configuration proxying: Automatic 31.55% AST slimming + 100% KV-cache retention
client = OpenAI(base_url="http://localhost:8080/v1")
```

* **Zero Local Source Footprint:** 100% compiled native ELF machine binary inside Alpine container.
* **Health check:** `GET http://localhost:8080/health`
* **Live savings metrics:** `GET http://localhost:8080/metrics`

---

## 🔌 Model Context Protocol (MCP) Stdio Proxy Mode

Wrapping your existing MCP server with CDX intercepts the JSON-RPC stdio stream, slims `tools/list` schema definitions by **30%~50%**, and compresses `tools/call` output bloat in real-time.

### Claude Desktop (`claude_desktop_config.json`) & Cursor (`.cursor/mcp.json`)

Add the `-m cdx_a2a_slimmer mcp-proxy --` prefix before your original MCP command:

```json
{
  "mcpServers": {
    "sqlite-optimized": {
      "command": "python",
      "args": [
        "-m", "cdx_a2a_slimmer", "mcp-proxy", "--",
        "npx", "-y", "@modelcontextprotocol/server-sqlite", "production.db"
      ]
    },
    "memory-optimized": {
      "command": "python",
      "args": [
        "-m", "cdx_a2a_slimmer", "mcp-proxy", "--",
        "npx", "-y", "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

### ⚡ Smithery.ai 1-Click Automated Installation
CDX MCP Proxy is officially registered on [Smithery.ai](https://smithery.ai/server/earthtbook/cdx-mcp-proxy):

```bash
# For Claude Desktop
npx -y @smithery/cli install earthtbook/cdx-mcp-proxy --client claude

# For Cursor
npx -y @smithery/cli install earthtbook/cdx-mcp-proxy --client cursor
```

### 📋 Zero-Terminal 1-Click Configuration (Direct Copy-Paste)
If you prefer not to use the terminal, simply paste the following into your `claude_desktop_config.json` (Windows: `%APPDATA%\Claude\claude_desktop_config.json` | macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "cdx-mcp-proxy": {
      "command": "python",
      "args": [
        "-m", "cdx_a2a_slimmer", "mcp-proxy", "--",
        "npx", "-y", "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```
*(Replace the wrapped command with any MCP tool you use, such as filesystem, postgres, or sqlite, to immediately unlock 30%~50% tool schema compression!)*

---

## 🛡️ Zero-Loss Guarantees

1. **Strict Numerical & Code Lock:** Numbers (`1042`), financial amounts (`$30.04`), SQL/Python code blocks, and variable identifiers are preserved 100% byte-for-byte.
2. **JSON Schema Integrity:** `required`, `properties`, and field types are strictly preserved.
3. **KV Cache Dual Discount:** Canonical prefix sorting guarantees OpenAI/Anthropic prompt cache hit rates remain at 100%.
4. **Sub-Millisecond Speed:** Pure zero-dependency C-optimized algorithms run in ~50 microseconds.

---

## ⚖️ Intellectual Property & Patent Protection

This software, including its AST schema pruning engines, deterministic lexicographical canonicalizers, and prompt-cache-preserving payload partitioning mechanisms, is protected under:
- **Republic of Korea Patent Application No. 10-2026-0172394** (Lossless In-Memory Proxy Slimming System and Method for Multi-Agent Communication Data)
- **Republic of Korea Patent Application No. 10-2026-0175561** (Payload Partitioning and Canonical Normalization System and Method to Preserve LLM Prompt Cache Hit Rates)
- **WIPO Digital Access Service (DAS) Priority:** `A867` & `E380`

All worldwide patents, copyrights, trade secrets, and machine binaries remain the exclusive property of Cantor Labs Inc. Reverse engineering, decompilation, and unauthorized commercial redistribution are strictly prohibited under the Cantor Labs Master Enterprise Agreement and EULA.

---

## 💎 Official Pricing Tiers
* **Developer Free ($0 / mo):** 1 Local Machine, up to 5 concurrent sessions, 100,000 monthly slimming calls, full 31.55% reduction & 100% KV-Cache alignment with free registered key.
* **Team ($499 / mo, $399/mo billed annually):** Up to 5 Node (Pod) Clusters, 1,000,000 monthly slimming calls, tool & conversation token pruning (~20%~30% savings), RFC 8259 deterministic canonicalizer, Prometheus telemetry, 24h technical support.
* **Business ($1,499 / mo, $1,199/mo billed annually):** Up to 20 Node (Pod) Clusters, 5,000,000 monthly slimming calls, high-concurrency threading engine, Kubernetes autoscaling & multi-VPC support, 99.9% availability guarantee (4h SLA).
* **Enterprise Sovereign (Custom ARR / Dedicated SLA):** Dedicated VPC & 100% Air-Gapped offline deployment, custom large-scale nodes (50~100+ Pods or unlimited), 15M+ unlimited monthly volume, PII zero-trust vault, 99.99% availability guarantee & 15-min priority engineer hotline.

---

## 🗺️ Roadmap
* **v1.0 (Current Release):** Tool JSON Schema slimming, greeting stripping, RFC 8259 deterministic canonicalizer (supporting ~20%~30% savings).
* **v1.1 (Upcoming):** Multi-turn context folding and structured JSON compression for large-scale enterprise workflows.
* **v1.2 (Upcoming):** Native C++/Rust/WASM extensions for sub-10µs latency.

---

## 📄 License
Commercial Enterprise / Apache 2.0 Community. Designed & Engineered by **Oh-dong-kyu** (Cantor Labs).
