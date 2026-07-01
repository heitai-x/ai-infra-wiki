---
title: RLHF And PPO Papers
type: source
source_type: paper
source_url: https://arxiv.org/abs/2203.02155
topic: training
component: rl-post-training
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [paper, rlhf, ppo, grpo, reward-model]
---

# RLHF And PPO Papers

## Why It Matters

`20-training-systems/rl-post-training-infra` 的系统设计必须理解 RLHF/PPO/GRPO 的算法结构：rollout、reward、advantage、KL、policy update 决定 GPU/rollout 比例和稳定性边界。

## Key Claims

- InstructGPT / RLHF 论文提出 reward model、policy model 和 KL 约束的整体框架。
- PPO 论文给出 clipped objective、advantage estimate 和 update epoch 的标准做法。
- GRPO / RLOO / ReMax 等后续工作讨论去掉 critic 的优势估计和工程简化。
- 论文明确 KL、reward、advantage、policy loss 的相互关系。
- 论文讨论 sample efficiency、stability、reward hacking 风险。

## Limits Or Caveats

- 论文给出的 reward / KL 数值是当时 setup 的结果，不能直接外推到所有模型和工作负载。
- 实际 RL infra 需要考虑长 rollout、超时、verifier、tool call 和 rejection sampling。
- policy update 频率、KL 目标和 reward shaping 会显著影响稳定性，论文仅给出原则。
- 引用时需要明确是 PPO / GRPO / DPO / ReMax 中的哪一个。

## Links To Concepts

- [[20-training-systems/rl-post-training-infra]]
- [[30-inference-systems/llm-serving-map]]
- [[20-training-systems/distributed-training-map]]

## Follow Up

- 后续按 PPO / GRPO / DPO 分别建独立 source card。
- 后续补 rollout/training 资源比例经验值来源。
