# Study Checkpoints

Checkpoint 保存一次学习任务的状态快照，便于不同 Agent 或不同时间的学习会话继续同一个主题。

使用方式：

1. 复制 `template.yml`。
2. 修改 `checkpoint_id`、目标、已加载页面和当前进度。
3. 在 `evidence` 中记录代码、实验、日志和回答路径。
4. 在 `next` 中记录下一步动作和需要加载的 stage。
5. 用 `scripts/check_learning.py` 查看 checkpoint 与 checklist 的汇总。

Checkpoint 与 Git 一起保存，内容保持人类可读。一个主题可以拥有多个按日期或阶段命名的 checkpoint。
