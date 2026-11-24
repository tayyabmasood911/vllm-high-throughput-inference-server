# ==============================================================================
# Production Dockerfile: vLLM High-Throughput Distributed Inference Server
# Features: PagedAttention, Ray Distributed Clustering, CUDA Acceleration
# ==============================================================================
FROM vllm/vllm-openai:v0.6.3.post1

LABEL maintainer="Tayyab Masood <tayyabmasood911@gmail.com>"
LABEL description="High-throughput distributed LLM serving engine powered by PagedAttention and Ray"

# Set runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    MODEL="meta-llama/Meta-Llama-3-8B-Instruct" \
    TENSOR_PARALLEL_SIZE=1 \
    PIPELINE_PARALLEL_SIZE=1 \
    MAX_MODEL_LEN=8192 \
    GPU_MEMORY_UTILIZATION=0.90 \
    MAX_NUM_SEQS=256 \
    SWAP_SPACE=4 \
    PORT=8000 \
    HOST=0.0.0.0

WORKDIR /workspace

# Install system monitoring and health probe tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=15s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE 8000 6379 8265

ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]
CMD ["--model", "meta-llama/Meta-Llama-3-8B-Instruct", \
     "--tensor-parallel-size", "1", \
     "--max-model-len", "8192", \
     "--gpu-memory-utilization", "0.90", \
     "--max-num-seqs", "256", \
     "--swap-space", "4", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
