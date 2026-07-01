---
title: RL Post Training Infra
type: concept
topic: training
component: rl-post-training
level: advanced
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [rlhf, grpo, ppo, slime, rollout, reward]
source_refs: [70-sources/official-docs]
---

# RL Post Training Infra

## 一句话

RL post-training 把训练系统和推理系统耦合起来：policy 训练需要 rollout serving、reward/verifier、采样、过滤、优势估计、梯度更新和数据闭环。

## 系统组件

```text
prompt dataset
  -> rollout workers / inference server
  -> reward model or rule verifier
  -> advantage estimation
  -> policy update with FSDP/Megatron backend
  -> evaluation and data filtering
```

## 与预训练不同的地方

- 训练 step 前需要生成样本，serving throughput 直接影响训练吞吐。
- reward/verifier 可能是模型、规则、工具调用或人工反馈。
- 多轮 agent/tool 场景会引入环境状态和超时。
- rollout 与 training 的资源比例需要动态调度。
- 数据质量和过滤策略影响稳定性。

## 关键指标

- rollout tokens/sec。
- reward latency 和失败率。
- samples accepted / filtered。
- KL、reward、advantage、policy loss。
- training step time。
- GPU allocation between rollout and training。

## 常见失败模式

- rollout server 成为瓶颈，训练 GPU 等数据。
- reward/verifier 不稳定导致样本质量抖动。
- policy 更新太快，KL 爆炸。
- 多机 rollout 与 training 资源争抢。
- checkpoint/resume 没保存采样状态。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/key-papers/rlhf-ppo-papers]]

## 相关页面

- [[20-training-systems/distributed-training-map]]
- [[30-inference-systems/llm-serving-map]]
- [[00-index/skill-index]]
