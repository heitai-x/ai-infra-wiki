---
title: Expert Parallel MoE
type: concept
topic: training
component: moe
level: advanced
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [moe, expert-parallel, all-to-all, routing]
source_refs: [70-sources/official-docs/megatron-core-docs, 70-sources/key-papers/gshard-paper, 70-sources/key-papers/switch-transformer-paper]
---

# Expert Parallel MoE

## 一句话

MoE 用多个 expert 扩大参数量，但每个 token 只激活少数 expert。Expert Parallel 把 expert 分布到不同 GPU，核心系统挑战是 routing、all-to-all、负载均衡和 capacity 控制。

## MoE FFN 流程

```text
tokens -> router/gate -> top-k experts
  -> dispatch tokens to expert ranks
  -> expert FFN compute
  -> combine outputs
```

## 关键状态

- Router weights：决定 token 到 expert 的分配。
- Expert weights：通常比 dense FFN 多很多。
- Dispatch buffer：按 expert 重排 token。
- Combine buffer：把 expert 输出还原到 token 顺序。
- Auxiliary loss / load balancing state：避免 expert 热点。

## Expert Parallel

EP 把不同 expert 放到不同 rank。token 根据 router 结果跨 rank 发送，常见通信是 all-to-all。

优点：参数容量扩展。代价：

- all-to-all 对网络和拓扑敏感。
- token routing 不均会造成 straggler。
- 在有容量上限或 overflow 策略的 MoE 中，capacity factor 过小可能 drop token 或降低质量；dropless MoE 不一定 drop token，但仍会面对 padding、负载不均或延迟放大的代价。
- 推理中热门 expert 会造成服务端负载不均。

## 训练问题

- router collapse：少数 expert 被过度选择。
- expert imbalance：某些 rank 计算时间明显更长。
- all-to-all traffic：跨节点通信成为 step bottleneck。
- checkpoint：expert shard 的保存和恢复更复杂。

## 推理问题

- batch 内 token 分布随机，expert 并发不稳定。
- 多租户 serving 时不同请求可能热点不同。
- expert cache、replication、placement 成为平台策略问题。

## 观测点

- 每个 expert token count。
- all-to-all bytes 和 latency。
- rank-wise step time。
- dropped token / capacity overflow。
- router entropy 和 auxiliary loss。

## 本地证据

- 暂无 `raw-sources/` 下的 expert token 分布、all-to-all latency、router entropy 复现样本。
- 章节中 MoE 状态、EP 通信代价、router collapse / imbalance 描述属于对 Megatron-Core 文档 + GShard / Switch Transformer 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/moe-<hw>-<commit>.md`，含 expert token 分布、all-to-all bytes、rank-wise step time、auxiliary loss 曲线。

## 尚未本地验证的边界

- “token routing 不均会造成 straggler”是经验结论，未给出具体 drop / 延迟放大的本机数字。
- dropless MoE 与 capacity overflow 的代价比较，本页未引用任何本地样本。
- “热门 expert replication”是平台策略方向，没有具体收益数字。

## 来源

- [[70-sources/official-docs/megatron-core-docs]]
- [[70-sources/key-papers/gshard-paper]]
- [[70-sources/key-papers/switch-transformer-paper]]

## 相关页面

- [[30-inference-systems/disaggregated-and-moe-serving]]
- [[10-foundations/nccl-and-networking]]
- [[20-training-systems/training-performance-playbook]]
