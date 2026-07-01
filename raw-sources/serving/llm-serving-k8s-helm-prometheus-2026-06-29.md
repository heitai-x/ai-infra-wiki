---
title: LLM Serving Kubernetes Helm Values And Prometheus Rules
type: raw
topic: serving
component: kubernetes
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [raw, serving, kubernetes, helm, prometheus, vllm]
artifact:
  kind: config
  source: local-simulated
  collected_at: 2026-06-29
  framework: vllm
  framework_commit: vllm-0.5.0-cuda12.1
  hardware: 2x A100-40GB single node, NVLink
  driver: 535.129.03
  cuda: 12.1
  command: helm install llm-runtime ./charts/vllm -f values.yaml
  raw_output: raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.yaml
  sha256: pending
related_sources:
  - 70-sources/official-docs/vllm-docs
  - 70-sources/official-docs/kserve-docs
  - 70-sources/official-docs/nvidia-k8s-device-plugin-docs
  - 70-sources/official-docs/slo-observability-docs
related_concepts:
  - 40-serving-platform/gpu-scheduling-kubernetes
  - 40-serving-platform/serving-platform-map
  - 40-serving-platform/observability-slo-cost
related_playbooks:
  - 80-playbooks/serving-production-deployment
  - 80-playbooks/serving-capacity-planning
note: |
  本 artifact 的 source 标记为 local-simulated，表示 Helm values 和 Prometheus rules 是基于 vLLM / KServe 文档的示例配置，而非从某次真实集群部署中抓取。
  作用是让 Wiki 提前具备可被引用的 raw artifact 结构；一旦获得真实部署输出，请按 raw-source-note-template 复制为新版本。
---

# LLM Serving Kubernetes Helm Values And Prometheus Rules

## 来源

- 命令：`helm install llm-runtime ./charts/vllm -f values.yaml`
- 框架 / Commit：vLLM 0.5.0 + CUDA 12.1
- 硬件：2 × A100-40GB，单机 NVLink
- 关联 source card：[[70-sources/official-docs/vllm-docs]]、[[70-sources/official-docs/kserve-docs]]、[[70-sources/official-docs/nvidia-k8s-device-plugin-docs]]、[[70-sources/official-docs/slo-observability-docs]]
- 关联概念页：[[40-serving-platform/gpu-scheduling-kubernetes]]、[[40-serving-platform/serving-platform-map]]、[[40-serving-platform/observability-slo-cost]]
- 关联 playbook：[[80-playbooks/serving-production-deployment]]、[[80-playbooks/serving-capacity-planning]]

## 原始输入

Helm `values.yaml`：

```yaml
replicaCount: 2
image:
  repository: vllm/vllm-openai
  tag: 0.5.0
  pullPolicy: IfNotPresent
resources:
  limits:
    nvidia.com/gpu: 1
    memory: 32Gi
  requests:
    nvidia.com/gpu: 1
    memory: 32Gi
extraArgs:
  - "--tensor-parallel-size=1"
  - "--gpu-memory-utilization=0.90"
  - "--max-model-len=4096"
  - "--max-num-seqs=128"
  - "--enable-prefix-caching"
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 120
  periodSeconds: 10
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 300
  periodSeconds: 30
nodeSelector:
  nvidia.com/gpu.product: A100-SXM4-40GB
```

Prometheus rules：

```yaml
groups:
  - name: llm-serving-slo
    rules:
      - alert: LLMHighTTFT
        expr: histogram_quantile(0.95, sum(rate(vllm_request_latency_seconds_bucket{phase="prefill"}[5m])) by (le)) > 2.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "TTFT p95 > 2s"
      - alert: LLMHighTPOT
        expr: histogram_quantile(0.95, sum(rate(vllm_request_latency_seconds_bucket{phase="decode"}[5m])) by (le)) > 0.15
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "TPOT p95 > 150ms"
      - alert: LLMKVCacheExhaustion
        expr: vllm_gpu_cache_usage_perc > 0.95
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "KV cache usage > 95%"
      - alert: LLMHighErrorRate
        expr: sum(rate(vllm_request_total{status="error"}[5m])) / sum(rate(vllm_request_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate > 5%"
      - alert: LLMQueueBacklog
        expr: vllm_running_seqs > 100 or vllm_waiting_seqs > 50
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Queue backlog high"
```

## 解读

- 结论 1：Helm values 中的 `readinessProbe.initialDelaySeconds=120` 和 `livenessProbe.initialDelaySeconds=300` 反映了模型加载慢的事实，与 [[40-serving-platform/gpu-scheduling-kubernetes]] 中"模型加载慢，扩容不是瞬时的"方向一致。
- 结论 2：Prometheus rules 覆盖了 [[40-serving-platform/observability-slo-cost]] 中定义的关键 SLO 指标：TTFT、TPOT、KV cache、error rate、queue。
- 边界：配置为 local-simulated，真实集群的 Helm chart 结构、metric 名称、告警阈值会随 vLLM 版本和业务 SLO 变化。

## 复现步骤

1. 准备 Kubernetes 集群，安装 NVIDIA device plugin 和 DCGM exporter。
2. 构建或拉取 vLLM 0.5.0 image。
3. 用 `helm install` 部署，根据真实模型和 GPU 调整 `--tensor-parallel-size`、`--gpu-memory-utilization`、`--max-model-len`。
4. 部署 Prometheus + Grafana，导入上述 rules。
5. 用真实输出覆盖本文件，复制为新版本 raw artifact。

## 引用建议

- 在 [[40-serving-platform/gpu-scheduling-kubernetes]] 的 "本地证据" 段直接引用本文件。
- 在 [[40-serving-platform/observability-slo-cost]] 的 "本地证据" 段直接引用本文件。
- 在 [[80-playbooks/serving-production-deployment]] 中作为部署清单对照样例。
