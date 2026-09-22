# Learning Bundles

Bundle 将一个学习目标组织成 bootstrap、map、core、practice、deep_dive 和 verify 阶段。

当前主题包：

- `inference-mha-kv-cache.yml`：MHA、GQA、KV Cache 和 serving。
- `training-ddp-fsdp.yml`：DDP、FSDP、ZeRO 和训练显存。
- `training-nccl-performance.yml`：NCCL、拓扑、通信和训练性能。
- `serving-capacity-planning.yml`：KV capacity、调度、SLO 和部署。
- `rag-wiki-retrieval.yml`：Wiki ingestion、检索、引用和评测。

查看一个主题的阶段：

```bash
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --list-stages
```

加载一个阶段：

```bash
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --stage core
```
