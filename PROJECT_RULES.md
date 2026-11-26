<!-- shared-agent-skills:start -->
## 跨项目共享技能规则（所有 AI 必读）

- 统一技能源：`https://github.com/sxy3481841323-ship-it/agent-skills`；本机位置为与本项目平级的 `../agent-skills/`。
- 开始创意、设计、3D、动效或游戏任务前，先读 `../agent-skills/AGENTS.md` 和相应技能；若共享库尚未克隆，先克隆到该平级目录。
- 所有新装、导入或创建的通用技能，必须完整存入 `../agent-skills/skills/<skill-name>/`，更新索引、验证后保存到共享仓库，再同步到 Agent 全局目录。不得只装在某个项目或某一台电脑后不回传。
- 项目 `.agents/skills/` 只允许真正项目专属的技能。不要复制通用技能，也不要用本项目规则覆盖其他项目。
- 通过 `python3 ../agent-skills/sync_skills.py --agent codex`、`--agent antigravity` 或 `--agent claude-code` 安装；其他客户端用 `--target` 指定实际技能目录。已有文件默认保留，同名冲突先核对。
- 项目业务约束、用户明确指令和现有未提交改动始终优先。不会自动识别全局技能的客户端，应直接读取共享库中完整的技能目录。
<!-- shared-agent-skills:end -->
