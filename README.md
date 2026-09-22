# AI Infra Training and Inference Learning Workspace

This project is the shared workspace for studying AI infrastructure, especially
training and inference systems.

Main artifact:

- [AI Infra LLM Wiki](ai-infra-wiki/README.md): a local Markdown / Obsidian-style
  systematic wiki for training systems, inference systems, serving platforms,
  RAG/agent infrastructure, experiments, source cards, and maintenance workflow.

Installed support:

- `codegraph` for static Python code structure visualization.
- Codex skills from `yzlnew/infra-skills`.
- Codex skills from `BBuf/AI-Infra-Auto-Driven-SKILLS`.

Project protocols:

- Progressive loading bundles: `packs/`.
- Reusable task prompts: `prompts/`.
- Tool capability manifest: `tools/manifest.yml`.
- Learning checklists and checkpoints: `checklists/` and `checkpoints/`.

Example:

```bash
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --stage core
python scripts/check_learning.py --checklist checklists/inference-mha-kv-cache.yml
```

Typical study tracks:

- Distributed training systems and memory planning.
- LLM serving, capacity planning, benchmarking, and incident triage.
- Profiler-driven performance analysis.
- SGLang/vLLM optimization loops.
- GPU kernel and model architecture exploration.
