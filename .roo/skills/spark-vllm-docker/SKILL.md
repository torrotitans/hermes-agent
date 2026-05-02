---
name: spark-vllm-docker
description: Build and deploy vLLM inference clusters on DGX Spark hardware using Docker, Ray, and RDMA/InfiniBand. USE FOR: vLLM deployment, DGX Spark, multi-node inference, Ray cluster, RDMA networking, NCCL configuration, model serving, GPU inference, distributed inference, flashinfer, fastsafetensors, cluster launch scripts, hf-download, benchmarking. DO NOT USE FOR: Kubernetes deployment (use kubernetes-deploy), general Docker builds (use docker-container), non-Spark hardware.
---

# Spark vLLM Docker Skill

## When to Use
- Deploying vLLM inference on DGX Spark single-node or multi-node clusters
- Building optimized Docker images for GPU inference workloads
- Configuring Ray-based distributed inference across multiple Spark nodes
- Setting up RDMA/InfiniBand networking for high-performance GPU communication
- Running large language models with fastsafetensors loading optimization
- Benchmarking LLM inference performance on DGX hardware

## When NOT to Use
- Kubernetes-based deployments (use kubernetes-deploy skill)
- General Docker container builds without GPU/RDMA requirements (use docker-container skill)
- Non-Spark hardware configurations
- CPU-only inference workloads

## Prerequisites
- DGX Spark hardware (single or multi-node)
- Docker CLI installed and accessible
- Passwordless SSH configured between cluster nodes
- Network connectivity between nodes (InfiniBand/RoCE)
- HuggingFace CLI token for model downloads

## Workflow

### 1. Clone Repository

```bash
git clone https://github.com/eugr/spark-vllm-docker.git
cd spark-vllm-docker
```

### 2. Build Docker Image

**Single Node:**
```bash
./build-and-copy.sh
```

**Multi-Node Cluster:**
```bash
./build-and-copy.sh -c
```

**Build Options:**
| Flag | Description |
| :--- | :--- |
| `--rebuild-vllm` | Build vLLM from source (latest main branch) |
| `--vllm-ref <tag>` | Build specific vLLM version/tag |
| `--rebuild-flashinfer` | Build FlashInfer from source |
| `--flashinfer-ref <tag>` | Build specific FlashInfer version |
| `--gpu-arch <arch>` | Target GPU architecture (default: `12.1a` for GB10) |
| `-c` | Copy image to all cluster nodes |

### 3. Download Model

**Local Download:**
```bash
./hf-download.sh QuantTrio/MiniMax-M2-AWQ
```

**Download and Distribute to Cluster:**
```bash
./hf-download.sh -c QuantTrio/MiniMax-M2-AWQ --copy-parallel
```

**Options:**
| Flag | Description |
| :--- | :--- |
| `-c` | Copy model to cluster nodes after download |
| `--copy-parallel` | Copy to all hosts concurrently |
| `-u <user>` | SSH username for remote copies |
| `--config <file>` | Custom .env configuration file |

### 4. Launch vLLM Cluster

**Single Node (Solo Mode):**
```bash
./launch-cluster.sh --solo exec \
  vllm serve \
    QuantTrio/Qwen3-VL-30B-A3B-Instruct-AWQ \
    --port 8000 --host 0.0.0.0 \
    --gpu-memory-utilization 0.7 \
    --load-format fastsafetensors
```

**Multi-Node Cluster:**
```bash
./launch-cluster.sh exec vllm serve \
  QuantTrio/MiniMax-M2-AWQ \
  --port 8000 --host 0.0.0.0 \
  --gpu-memory-utilization 0.7 \
  -tp 2 \
  --distributed-executor-backend ray \
  --max-model-len 128000 \
  --load-format fastsafetensors \
  --enable-auto-tool-choice --tool-call-parser minimax_m2
```

### 5. Configuration via .env

Create `.env` file in project root:

```bash
# Cluster Configuration
COPY_HOSTS=192.168.1.1,192.168.1.2
VLLM_MEMORY_UTILIZATION=0.7
VLLM_PORT=8000

# Model Configuration
MODEL_NAME=QuantTrio/MiniMax-M2-AWQ
TENSOR_PARALLEL_SIZE=2
MAX_MODEL_LEN=128000

# Network Configuration
NCCL_SOCKET_IFNAME=eth0
NCCL_IB_DISABLE=0
```

## Configuration Details

### Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `VLLM_MEMORY_UTILIZATION` | `0.7` | GPU memory utilization ratio |
| `VLLM_PORT` | `8000` | Serving port for vLLM |
| `TENSOR_PARALLEL_SIZE` | `1` | Number of GPUs for tensor parallelism |
| `MAX_MODEL_LEN` | `32768` | Maximum sequence length |
| `NCCL_SOCKET_IFNAME` | `eth0` | Network interface for NCCL |
| `NCCL_IB_DISABLE` | `0` | Enable InfiniBand (1=disable) |

### Launch Scripts

Create custom launch scripts in `examples/` directory:

```bash
#!/bin/bash
# PROFILE: OpenAI GPT-OSS 120B
# DESCRIPTION: vLLM serving with FlashInfer MOE optimization

export VLLM_USE_FLASHINFER_MOE_MXFP4_MXFP8=1

vllm serve openai/gpt-oss-120b \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 2 \
    --distributed-executor-backend ray
```

Use with:
```bash
./launch-cluster.sh --launch-script examples/vllm-openai-gpt-oss-120b.sh
```

## Examples

### Example 1: Single Node Qwen3-VL

```bash
./launch-cluster.sh --solo exec \
  vllm serve QuantTrio/Qwen3-VL-30B-A3B-Instruct-AWQ \
  --port 8000 --host 0.0.0.0 \
  --gpu-memory-utilization 0.7 \
  --load-format fastsafetensors
```

### Example 2: Multi-Node MiniMax-M2

```bash
# Download and distribute
./hf-download.sh QuantTrio/MiniMax-M2-AWQ -c --copy-parallel

# Launch cluster
./launch-cluster.sh exec vllm serve \
  QuantTrio/MiniMax-M2-AWQ \
  --port 8000 --host 0.0.0.0 \
  --gpu-memory-utilization 0.7 \
  -tp 2 \
  --distributed-executor-backend ray \
  --max-model-len 128000 \
  --load-format fastsafetensors
```

### Example 3: GLM-4.7 with Mod Patch

```bash
./launch-cluster.sh --launch-script examples/vllm-glm-4.7-nvfp4.sh \
  --apply-mod mods/fix-Salyut1-GLM-4.7-NVFP4
```

## Troubleshooting

### Container Exits Immediately
- Check logs: `docker logs vllm_node`
- Verify model path exists
- Check GPU memory availability: `nvidia-smi`

### RDMA/InfiniBand Not Working
- Verify IB interfaces: `ibstat`
- Check NCCL settings: `nvidia-smi topo -m`
- Ensure `NCCL_IB_DISABLE=0`

### Out of Memory (OOM)
- Reduce `--gpu-memory-utilization` (try 0.6)
- Reduce `--max-model-len`
- Use `--load-format fastsafetensors` for efficient loading

### Model Download Fails
- Check HuggingFace token: `huggingface-cli whoami`
- Verify network connectivity
- Use `--resume-download` flag

### Cluster Nodes Not Discovering Each Other
- Verify passwordless SSH: `ssh <node> hostname`
- Check network connectivity: `ping <node>`
- Review `.env` COPY_HOSTS configuration

## Acceptance Criteria

- [ ] Docker image builds successfully on head node
- [ ] Image is distributed to all cluster nodes (multi-node mode)
- [ ] Model downloads and distributes without errors
- [ ] vLLM serves on port 8000 and responds to health checks
- [ ] Multi-node inference utilizes all GPUs via Ray

## References

- [spark-vllm-docker Repository](https://github.com/eugr/spark-vllm-docker)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Ray Documentation](https://docs.ray.io/)
- [NVIDIA NCCL Documentation](https://docs.nvidia.com/deeplearning/nccl/)
