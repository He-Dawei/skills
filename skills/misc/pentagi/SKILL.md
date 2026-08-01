---
name: pentagi
description: Use when setting up or using PentAGI — an autonomous AI-powered penetration testing platform with multi-agent orchestration. Triggers: "pentest with AI", "autonomous security testing", "AI penetration testing", "set up PentAGI", "Docker pentest lab", "automated vulnerability assessment", "AI red team".
---

# PentAGI

Autonomous AI-powered penetration testing platform. Docker-based, multi-agent system with 20+ built-in security tools, knowledge graph memory, and support for 10+ LLM providers including local models via Ollama.

## Quick Reference

| Task | Command |
|------|---------|
| Install (Linux) | `mkdir pentagi && cd pentagi && wget -O installer.zip https://pentagi.com/downloads/linux/amd64/installer-latest.zip && unzip installer.zip && sudo ./installer` |
| Manual setup | Copy `.env.example` → `.env`, fill API keys, `docker compose up -d` |
| Web UI | `http://localhost:3000` |
| API (REST) | `http://localhost:3000/api/v1` |
| API (GraphQL) | `http://localhost:3000/api/graphql` |
| Grafana | `http://localhost:3001` |
| Langfuse | `http://localhost:3002` |

## Architecture

```
Security Engineer → Web UI / API → PentAGI → Target System
                                    ├── LLM Provider (OpenAI/Anthropic/Gemini/Ollama/Bedrock)
                                    ├── Search (Google/DuckDuckGo/Tavily/Perplexity/Sploitus)
                                    ├── Knowledge Graph (Graphiti + Neo4j)
                                    ├── Vector Store (PostgreSQL + pgvector)
                                    ├── Monitoring (Grafana/VictoriaMetrics/Jaeger/Loki)
                                    └── Analytics (Langfuse/ClickHouse)
```

### Agent Roles

| Agent | Role |
|-------|------|
| **Orchestrator** | Coordinates flow, delegates tasks to specialists |
| **Researcher** | Analyzes target, searches for vulnerabilities and CVEs |
| **Developer** | Plans attack strategy, selects tools and exploits |
| **Executor** | Runs pentest commands in sandboxed Docker containers |
| **Adviser/Mentor** | Monitors execution, intervenes when agent gets stuck |
| **Planner** | Decomposes complex tasks into 3-7 actionable steps |
| **Reflector** | Corrects failures, guides agents toward proper tool usage |

## System Requirements

- Docker + Docker Compose (or Podman)
- 2+ vCPU, 4GB+ RAM, 20GB disk
- At least one LLM provider API key

## LLM Provider Setup

### Cloud Providers

```bash
# .env — at least one required
OPEN_AI_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
```

### Local Models (Ollama)

```bash
# .env
OLLAMA_SERVER_CONFIG_PATH=./examples/configs/ollama-llama318b.provider.yml

# Pull and run
ollama pull llama3.1:8b
docker compose up -d
```

Create provider config at `examples/configs/ollama-llama318b.provider.yml`:
```yaml
provider: ollama
model: llama3.1:8b
base_url: http://host.docker.internal:11434
context_window: 131072
max_tokens: 4096
```

**Important for small models (< 32B)**: Enable execution monitoring and task planning for 2x quality improvement.

### Production: vLLM + Qwen3.5-27B-FP8

Use vLLM with Qwen3.5-27B-FP8 for air-gapped production deployments. See `examples/guides/vllm-qwen35-27b-fp8.md` in the repo.

## Key Configuration

### Execution Monitoring (Beta)

```bash
# .env — recommended for models < 32B
EXECUTION_MONITOR_ENABLED=true
EXECUTION_MONITOR_SAME_TOOL_LIMIT=5      # Trigger mentor after 5 identical calls
EXECUTION_MONITOR_TOTAL_TOOL_LIMIT=10    # Trigger mentor after 10 total calls
```

### Intelligent Task Planning (Beta)

```bash
AGENT_PLANNING_STEP_ENABLED=true          # Auto-decompose complex tasks
```

### Tool Call Limits

```bash
MAX_GENERAL_AGENT_TOOL_CALLS=100          # Orchestrator, Pentester, Coder
MAX_LIMITED_AGENT_TOOL_CALLS=20           # Searcher, Reporter, Adviser
```

### Search Engines

```bash
# At least one for information gathering
TAVILY_API_KEY=tvly-...
GOOGLE_API_KEY=... GOOGLE_CX=...
PERPLEXITY_API_KEY=...
DUCKDUCKGO_ENABLED=true                   # Free, no key needed
SPLOITUS_ENABLED=true                     # Exploit search, no key
SEARXNG_ENABLED=true                      # Self-hosted, no key
```

## Two-Node Production Architecture

For production: separate worker node isolates pentest execution from the main server.

```bash
# Worker node
docker run --rm -it \
  --privileged \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 2376:2376 \
  vxcontrol/pentest-worker:latest

# Main server .env
DOCKER_HOST=tcp://worker-ip:2376
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/certs
```

See `examples/guides/worker_node.md` in the repo.

## Built-in Security Tools

20+ tools in sandboxed containers: nmap, metasploit, sqlmap, hydra, john, hashcat, gobuster, ffuf, nikto, wpscan, nuclei, zaproxy, burpsuite, responder, impacket, crackmapexec, enum4linux, snmpwalk, dirb, dnsrecon, and more.

## Workflow

1. **Create Flow** in Web UI — name, target description, parameters
2. **Orchestrator** queries vector store for similar past tasks
3. **Researcher** analyzes target, searches CVEs and known vulnerabilities
4. **Developer** plans attack strategy based on findings
5. **Executor** runs tools in isolated Docker containers
6. **Reporter** generates detailed vulnerability report with exploitation guides
7. **Memory** stores successful approaches for future reuse

## API Access

Create Bearer tokens from Web UI `Settings → PentAGI API`:

```bash
# REST
curl -H "Authorization: Bearer pentagi-TOKEN" \
  http://localhost:3000/api/v1/flows

# GraphQL
curl -H "Authorization: Bearer pentagi-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ flows { id name status } }"}' \
  http://localhost:3000/api/graphql
```

## Common Mistakes

- **No search engine configured**: Agents can't gather target intelligence. At minimum enable `DUCKDUCKGO_ENABLED=true`.
- **Too small a model without supervision**: Models < 32B need `EXECUTION_MONITOR_ENABLED=true` + `AGENT_PLANNING_STEP_ENABLED=true` or they loop infinitely.
- **Single-node for real pentests**: Production pentesting needs two-node setup (worker isolation). Single-node is for lab/demo only.
- **Forgetting Docker-in-Docker privileges**: Worker containers need `--privileged` or proper capabilities.
- **Not configuring enough tool call budget**: Complex targets may need higher `MAX_GENERAL_AGENT_TOOL_CALLS`.

## Important

PentAGI is for **authorized security testing only**. Always have written permission before testing any target. Unauthorized penetration testing is illegal.
