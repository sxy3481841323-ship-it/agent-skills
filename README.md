# 跨项目 Agent Skills

一个独立维护的共享技能库，供 Codex、Antigravity、Claude Code、Gemini CLI 和其他支持 `SKILL.md` 的工具复用。它与各项目平级，项目继续维护自己的业务规则。

完整技能清单见 [CATALOG.md](CATALOG.md)，程序化入口见 [registry.json](registry.json)，所有 AI 应先阅读 [AGENTS.md](AGENTS.md)。

## 下载和安装

将共享仓库与自己的项目克隆到同一个工作目录：

```bash
git clone https://github.com/sxy3481841323-ship-it/agent-skills.git
cd agent-skills
python3 sync_skills.py --list
python3 sync_skills.py --agent antigravity --dry-run
python3 sync_skills.py --agent antigravity
```

| 客户端 | 安装命令 | 全局目录 |
| --- | --- | --- |
| Codex CLI | `python3 sync_skills.py --agent codex` | `~/.agents/skills` |
| Antigravity | `python3 sync_skills.py --agent antigravity` | `~/.gemini/config/skills` |
| Claude Code | `python3 sync_skills.py --agent claude-code` | `~/.claude/skills` |
| Gemini CLI | `python3 sync_skills.py --agent gemini-cli` | `~/.gemini/skills` |
| 其他客户端 / 自定义 harness | `python3 sync_skills.py --target /实际的技能目录` | 由该工具的配置决定 |

可重复 `--agent` 或 `--target`；用 `--skills game-brainstorm antialgorithm` 只安装选中的技能。原有技能默认保留，同名内容不同会报冲突；`--update` 只升级本脚本管理、且本地未被改动的安装副本，不会覆盖他人编辑。

ChatGPT 的账号级 Skills 需要通过 ChatGPT 自己的安装流程。GitHub 上存在文件或 CLI 复制成功，均不代表已经安装到 ChatGPT 账号。

全局目录按 `vercel-labs/skills` 的客户端定义核对；不同版本的客户端发现规则可能变化，自定义路径始终可用。

## 项目之前的统一规则

在 `agent-skills` 目录运行：

```bash
python3 sync_skills.py --workspace ..
```

这会在三个项目共同父目录的 `AGENTS.md` 中加入有边界标记的共享规则，保留原有内容。各项目的 `AGENTS.md` 仍应包含 [PROJECT_RULES.md](PROJECT_RULES.md) 的入口规则，因为部分客户端只读取当前 Workspace 内的规则。

所有新安装的通用技能都完整保存到 `agent-skills/skills/<name>/`，更新索引并保存到共享仓库，再安装到各 Agent 的全局目录。项目目录里不再维护通用技能的独立副本。

## 新技能回传

```bash
python3 sync_skills.py --import my-skill --source ~/.gemini/config/skills
python3 scripts/build_registry.py
python3 scripts/validate_library.py
git add skills/my-skill registry.json CATALOG.md checksums.sha256
git commit -m 'Add my-skill'
git push
```

导入保留整个技能目录并过滤环境文件、缓存和版本控制目录；检测到疑似密钥会拒绝导入。同名版本不一致时先比较，禁止覆盖。以上命令不安装依赖、不调用付费 API、不自动部署项目。

## 读取仓库与实际调用的区别

- **只参考方法、构思方案**：能访问 GitHub 的 Agent 可以直接读取 `skills/<name>/SKILL.md` 或索引里的 `raw_url`。
- **自动发现、运行脚本、使用模板/字体/资源**：下载完整仓库或完整技能目录，并放入该客户端支持的技能目录。只下载 `SKILL.md` 会缺少配套文件。
- **兄弟技能互调**：安装相关技能到同一个全局根目录；完整安装可保留平铺的兄弟目录关系。
- **第三方生成服务**：技能文件可读取和安装，不等于已开通 Tripo、ElevenLabs、Gemini 或其他外部服务。实际需要时再配置；平台已有原生图像或浏览器工具时优先使用。

## 来源与许可证

合并了 AI 雷达、幸福俱乐部里已保存的技能，并补充此前选定合集中的创意、设计、动效、3D 和演示类技能。保留同名技能的项目内较新完整版本；来源提交、原路径和原始元数据见 [source-inventory.json](source-inventory.json) 与各目录的 `references/upstream.json`。

本库的整理脚本使用 MIT；各技能、图片、字体和模板遵循各自原始许可证，参见 [LICENSE](LICENSE)。

## For other agents

Read `AGENTS.md`, discover skills using `registry.json`, and load only what the task needs. The canonical source is this repository; install complete directories into your host's supported skill path. Keep project rules in the project, preserve local changes, and publish newly installed reusable skills back here with provenance. Do not assume a remote Markdown read executes bundled scripts or installs dependencies.
