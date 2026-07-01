---
title: Serving Production Deployment
type: playbook
topic: serving
component: deployment
level: advanced
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [serving, kubernetes, canary, rollback, autoscaling]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/official-docs/kserve-docs, 70-sources/official-docs/ray-serve-docs, 70-sources/official-docs/nvidia-k8s-device-plugin-docs, 70-sources/official-docs/triton-inference-server-docs]
---

# Serving Production Deployment

## 目标

把一个 LLM runtime 从“能启动”变成“可上线”：有健康检查、容量护栏、灰度、回滚、观测、成本归因和事故响应。

## 最小部署清单

- Model artifact：权重、tokenizer、config、checksum、来源。
- Runtime image：框架、CUDA、driver、NCCL、commit。
- Launch command：所有 serving 参数。
- Resource request：GPU 数、CPU、内存、ephemeral storage。
- Health checks：启动、ready、liveness、model loaded。
- Metrics：TTFT、TPOT、queue、KV cache、GPU、error。
- Rollout：canary、traffic split、rollback 条件。
- Guardrail：max context、max concurrency、quota、rate limit。

## Kubernetes YAML 骨架

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-runtime
spec:
  replicas: 1
  selector:
    matchLabels:
      app: llm-runtime
  template:
    metadata:
      labels:
        app: llm-runtime
    spec:
      containers:
        - name: server
          image: <runtime-image>
          command: ["bash", "-lc"]
          args: ["<serve command>"]
          resources:
            limits:
              nvidia.com/gpu: 1
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
```

这只是骨架。真实生产需要结合 runtime 的 health endpoint、PVC/model cache、nodeSelector、topology、MIG、secrets、service mesh 和网关策略。

## Canary / Rollback

Canary 必须比较：

- 请求成功率。
- TTFT/TPOT p95/p99。
- queue time。
- GPU memory / KV free blocks。
- 输出质量 guardrail。
- 成本/token。

Rollback 条件要自动化，例如连续 5 分钟 error rate 或 p99 超过 SLO。

## Autoscaling

LLM serving 不适合只按 CPU 扩缩容。常见信号：

- queue length / queue time。
- running requests。
- KV cache free blocks。
- generation tokens/sec。
- p95 latency。
- GPU utilization 和 memory。

模型加载慢时，autoscaling 需要 warm pool 或提前扩容。

## 本地证据

- 暂无 `raw-sources/` 下的真实 canary / rollback 决策记录、autoscaling 曲线、incident 复盘样本。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/serving/rollout-<date>.md`，含 canary 决策记录、rollback 条件触发、autoscaling 曲线。

## 尚未本地验证的边界

- “LLM serving 不适合只按 CPU 扩缩容”是经验结论，本页未引用具体 autoscaling 对照。
- “模型加载慢时需要 warm pool”是策略方向，没有具体加载耗时数字。
- rollback 条件“连续 5 分钟 error rate 或 p99 超过 SLO”是示例阈值，真实阈值依赖业务容忍度。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/kserve-docs]]
- [[70-sources/official-docs/ray-serve-docs]]
- [[70-sources/official-docs/nvidia-k8s-device-plugin-docs]]
- [[70-sources/official-docs/triton-inference-server-docs]]

## 相关页面

- [[40-serving-platform/serving-platform-map]]
- [[40-serving-platform/gpu-scheduling-kubernetes]]
- [[80-playbooks/serving-capacity-planning]]
