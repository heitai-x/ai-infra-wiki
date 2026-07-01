---
title: Start Here
type: index
topic: ai-infra
level: beginner
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [onboarding, roadmap, index]
---

# Start Here

AI Infra 的训推系统可以用一句话概括：把模型训练和模型推理变成可扩展、可观测、可优化、可恢复、成本可控的系统工程。

## 先建立全局心智模型

一条训练 step 通常包括：

1. 数据读取和预处理。
2. forward 计算 activation。
3. loss 和 backward 产生梯度。
4. 梯度通信和参数/状态同步。
5. optimizer 更新参数。
6. checkpoint、日志、metric、容错状态持久化。

一条推理请求通常包括：

1. 请求进入网关和调度器。
2. tokenizer / routing / admission control。
3. prefill 处理 prompt。
4. decode 按 token 迭代生成。
5. KV cache 分配、复用、换出或回收。
6. streaming 返回、计量、日志、SLO 观测。

## 第一轮阅读顺序

1. [[01-roadmap/ai-infra-skill-tree]]
2. [[01-roadmap/competency-matrix]]
3. [[10-foundations/gpu-system-map]]
4. [[10-foundations/nccl-and-networking]]
5. [[20-training-systems/distributed-training-map]]
6. [[20-training-systems/ddp-fsdp-zero]]
7. [[20-training-systems/tensor-pipeline-context-parallel]]
8. [[30-inference-systems/llm-serving-map]]
9. [[30-inference-systems/kv-cache-paged-attention]]
10. [[30-inference-systems/batching-scheduling]]
11. [[40-serving-platform/observability-slo-cost]]

## 最小实践闭环

完成下面三个小项目，才算真正入门：

1. 单机多卡训练：跑一个小模型 DDP/FSDP，对比显存、step time、通信时间。
2. LLM serving benchmark：用 vLLM 或 SGLang 部署一个 7B/14B 模型，测 TTFT、TPOT、吞吐和显存。
3. 一次排障演练：制造 OOM、NCCL timeout、KV cache 不足、请求排队四类问题，并记录证据链。

## 学习时强制问的问题

- 这个机制解决的是显存、计算、通信、IO、调度还是可靠性问题？
- 它移动了哪些张量？张量 shape 和 dtype 是什么？
- 它增加了什么同步点？能不能 overlap？
- 它的瓶颈在哪个硬件资源：SM、HBM、NVLink、PCIe、NIC、CPU、磁盘？
- 它在单机、单机多卡、多机多卡下行为有什么不同？
- 它如何被 metric、trace、log 或 benchmark 证明？
