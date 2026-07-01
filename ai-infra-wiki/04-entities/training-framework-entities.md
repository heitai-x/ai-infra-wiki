---
title: Training Framework Entities
type: entity
source_type: curated
entity_type: framework

topic: training
component: frameworks
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [entities, training-frameworks, pytorch, deepspeed, megatron]
---

# Training Framework Entities

## 本地证据

- 暂无 `raw-sources/` 下的 PyTorch Distributed / DeepSpeed / Megatron-Core / NeMo / Ray Train 版本对比与本机配置样本。
- 实体页中的角色、关键概念、最佳学习入口属于对官方文档与 README 的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/frameworks-entities-<commit>.md`，含 PyTorch Distributed / DeepSpeed / Megatron-Core 的 version / commit / 安装路径与基本 import 自检。

## 尚未本地验证的边界

- NeMo / Ray Train 仍标“后续补 source card”，未给出 source_refs，本页对该段维持 medium。
- “最佳学习入口” 是经验判断，不构成 framework 官方学习路径。

## 实体清单

### PyTorch Distributed

- Role: 基础分布式训练 API 和运行时抽象。
- Main concepts: process group、DDP、FSDP、DTensor、distributed checkpoint。
- Best for learning: 从最小 DDP/FSDP 实验理解状态切分和 collective。
- Links: [[60-frameworks/pytorch-distributed]], [[20-training-systems/ddp-fsdp-zero]]。

## DeepSpeed

- Role: 大模型训练优化框架，尤其是 ZeRO 和 offload。
- Main concepts: ZeRO-1/2/3、CPU/NVMe offload、activation checkpointing、engine config。
- Best for learning: 显存优化、配置驱动训练和 ZeRO 实践。
- Links: [[60-frameworks/deepspeed-megatron]], [[20-training-systems/ddp-fsdp-zero]]。

## Megatron-Core / Megatron-LM

- Role: NVIDIA 大模型训练核心组件和参考训练框架。
- Main concepts: TP、PP、CP/SP、EP、distributed optimizer、MoE。
- Best for learning: 大模型模型并行和多维并行组合。
- Links: [[60-frameworks/deepspeed-megatron]], [[20-training-systems/tensor-pipeline-context-parallel]]。

## NeMo

- Role: NVIDIA 训练和推理生态中的高层框架，常与 Megatron-Core 结合。
- Main concepts: 大模型训练 recipe、数据处理、checkpoint、部署衔接。
- Status: 后续补 source card。
- Links: [[99-maintenance/backlog]]。

## Ray Train

- Role: Ray 生态中的分布式训练编排。
- Main concepts: worker、scaling config、fault tolerance、Ray Data 集成。
- Status: 后续补 source card。
- Links: [[99-maintenance/backlog]]。
