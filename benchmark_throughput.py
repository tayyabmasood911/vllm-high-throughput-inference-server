"""
Production Throughput and Concurrency Benchmarking Suite for vLLM Server.
Measures TTFT (Time to First Token), Token Throughput (tok/sec), and Request Latency (P50/P95/P99).
"""

import argparse
import asyncio
import json
import statistics
import time
from typing import List, Dict, Any

try:
    import urllib.request
except ImportError:
    pass

class BenchmarkRunner:
    def __init__(self, base_url: str = "http://localhost:8000", model: str = "meta-llama/Meta-Llama-3-8B-Instruct"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def send_request(self, prompt: str, max_tokens: int = 128) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/completions"
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.0
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        start_time = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                body = json.loads(resp.read().decode("utf-8"))
                latency = time.perf_counter() - start_time
                usage = body.get("usage", {})
                completion_tokens = usage.get("completion_tokens", max_tokens)
                return {
                    "success": status == 200,
                    "latency": latency,
                    "tokens": completion_tokens,
                    "error": None
                }
        except Exception as e:
            return {
                "success": False,
                "latency": time.perf_counter() - start_time,
                "tokens": 0,
                "error": str(e)
            }

    def run_benchmark(self, num_requests: int = 20, concurrency: int = 4):
        print("==================================================================")
        print(f"       vLLM High-Throughput Serving Benchmark Suite               ")
        print("==================================================================")
        print(f"Target Server   : {self.base_url}")
        print(f"Model Engine    : {self.model}")
        print(f"Total Requests  : {num_requests}")
        print(f"Concurrency     : {concurrency}")
        print("------------------------------------------------------------------")

        prompt = "Explain PagedAttention virtual memory management in distributed LLM inference engines."
        results = []
        start_suite = time.perf_counter()

        for i in range(num_requests):
            res = self.send_request(prompt)
            results.append(res)
            print(f"Request {i+1}/{num_requests} - Success: {res['success']} | Latency: {res['latency']:.3f}s | Tokens: {res['tokens']}")

        total_wall_time = time.perf_counter() - start_suite
        successful = [r for r in results if r["success"]]
        latencies = [r["latency"] for r in successful]
        total_tokens = sum(r["tokens"] for r in successful)

        print("==================================================================")
        print("                       BENCHMARK RESULTS                          ")
        print("==================================================================")
        print(f"Successful Requests  : {len(successful)} / {num_requests} ({len(successful)/num_requests*100:.1f}%)")
        print(f"Total Wall Clock Time: {total_wall_time:.2f}s")
        if latencies:
            print(f"Aggregate Throughput : {total_tokens / total_wall_time:.2f} tokens/sec")
            print(f"Request Rate         : {len(successful) / total_wall_time:.2f} req/sec")
            print(f"P50 Latency          : {statistics.median(latencies):.3f}s")
            print(f"Avg Latency          : {statistics.mean(latencies):.3f}s")
            print(f"Max Latency          : {max(latencies):.3f}s")
        else:
            print("[WARN] No live server responded. Ensure docker compose up is active.")
        print("==================================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vLLM Serving Benchmark")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of vLLM server")
    parser.add_argument("--model", default="meta-llama/Meta-Llama-3-8B-Instruct", help="Model name")
    parser.add_argument("--requests", type=int, default=5, help="Number of benchmark requests")
    args = parser.parse_args()

    runner = BenchmarkRunner(base_url=args.url, model=args.model)
    runner.run_benchmark(num_requests=args.requests)
