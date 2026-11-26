# 在 Mac 上补齐共享技能

这份清单供本机的 Antigravity 或 Codex 执行。GitHub 已保存完整源文件，不表示本机客户端已经安装；先补齐目录，再验证客户端识别。

## 可直接交给本机 AI 的任务

> 阅读当前项目的 AGENTS.md 与本文件。将 https://github.com/sxy3481841323-ship-it/agent-skills 作为共享母库，在当前项目的共同父目录中寻找或克隆 agent-skills；保留已有仓库、未提交修改和已有技能。使用共享库脚本补齐 Antigravity 与 Codex 的全局技能，在父目录安装共享规则，并验证客户端确实能识别、选用这些技能。现有同名内容有差异时保留原版并报告，不强制覆盖。若本机还有尚未回传的通用创意技能，核对来源和许可证后完整导入共享库并更新索引；有写入权限时提交回传，否则保留本机改动并说明。DeepSeek harness 只有在实际配置中找到技能目录后才使用 --target，不能猜路径。测试只做技能发现和构思，不调用付费 API、资讯抓取、回测或部署。结束时逐客户端给出真实的安装数量、冲突、识别结果与未完成事项。

## 执行步骤

1. 先读当前项目规则，只在当前工作区与其共同父目录定位相关项目和共享库。已有 `agent-skills` 时核对 origin；来源不同则保留，不覆盖。工作区干净时可以 `git pull --ff-only`；有改动则先报告，不自动清理或 stash。
2. 若尚无共享库，在项目共同父目录运行以下命令。仓库公开，下载本身不需要另一次 GitHub 登录。

   ```bash
   git clone https://github.com/sxy3481841323-ship-it/agent-skills.git
   cd agent-skills
   ```

3. 从本库目录先预览，再实际补齐。脚本复制完整技能目录，含脚本、引用、字体、模板和许可证。

   ```bash
   python3 sync_skills.py --agent antigravity --agent codex --dry-run
   python3 sync_skills.py --agent antigravity --agent codex
   python3 sync_skills.py --workspace ..
   ```

   默认目标：Antigravity 为 `~/.gemini/config/skills`，Codex 为 `~/.agents/skills`。其他客户端按本库 README 选择；自定义 harness 须使用其配置中的真实目录。

4. 脚本默认保留已有同名内容。退出码 2 表示存在冲突，应查看每个结果：不冲突的缺失项可能已经补齐，冲突项必须保留并核对。`--update` 只升级本脚本此前管理且本机未改过的副本；不能用它强制替换用户或其他 AI 的修改。
5. 如需回传本机新技能，用 `--import <name> --source <实际全局根目录>` 导入，补齐来源和许可证记录，再运行索引生成与校验。只提交本次内容，不提交账号、配置凭据或缓存；普通下载和调用不要求公开写入权限。

   ```bash
   python3 scripts/build_registry.py
   python3 scripts/validate_library.py
   ```

6. 当前项目在工作区干净时拉取云端新规则；有本机修改时保留并报告。量化、AI 雷达和幸福俱乐部的云端主分支已接入共享入口，新项目参照 `PROJECT_RULES.md` 接入。

## 验收标准

- **源文件**：共享库校验通过，配套资源完整。
- **本机目录**：分别记录各客户端实际新增、未变化与冲突的数量；核对所报目录确实是客户端配置使用的目录。
- **客户端识别**：通过该客户端的技能列表、加载记录或受支持界面确认。仅看到文件不等于已经被客户端识别。
- **只读调用**：让客户端选择合适技能，为“幸福俱乐部首页的灯光与互动”给出一个方案；说明实际读了哪些入口和引用，不调用外部生成服务。
- **如实交接**：未知的 harness 路径、未被识别的技能或外部依赖分别写为未完成，不把下载成功说成全平台全部可用。

ChatGPT 账号级 Skills 使用平台自己的安装与审核流程，本机脚本不替代该流程。
