---
name: shared-creative-skills
description: "跨项目共享创意技能库的统一调用入口。用于创意发散、产品构思、网页视觉、排版品牌、生成艺术、3D/Three.js、动效手势、游戏玩法、镜头与声效；也用于用户点名共享库中的某个技能。按任务查索引并加载完整说明和必要资源，优先遵守当前项目规则；新装通用技能须回传统一 GitHub 技能库。"
---

# Shared creative skills

Use https://github.com/sxy3481841323-ship-it/agent-skills as the canonical reusable skill library. This entry point selects and loads skills; it does not imply every library item is separately registered in ChatGPT's Skills picker.

## Resolve the library

1. Read the current project's AGENTS.md. Project constraints and the user's brief take priority over a skill's default style or workflow.
2. Locate a sibling `../agent-skills` checkout or another task-known checkout of that exact repository. Check its AGENTS.md and registry.json. Never overwrite an unrelated directory or discard local changes.
3. If no checkout is available, read registry.json using the connected GitHub tools. The bundled references/catalog.json is a discovery fallback and can be older than the repository. Use exact returned paths and refs when fetching files.
4. For instructions-only work, reading the selected SKILL.md and its required references remotely is sufficient. If scripts, images, templates, fonts or sibling imports are needed, obtain the complete repository or complete skill directories. Do not call a missing script or treat a remote Markdown read as an executed tool.

## Select and apply

- Honor an explicitly named skill. Resolve aliases through registry.json; `taste-skill` maps to `design-taste-frontend`.
- For an open-ended task, choose a small relevant combination. Useful examples: antialgorithm + design-thinking for directions; frontend-design + impeccable for interface design; game-brainstorm + game-feel for gameplay; threejs-game-director + the needed rendering skill for 3D games.
- Read the selected skill's full entry point and any references it declares necessary. Load other skills only when their guidance is needed.
- Use the host's actual tools. Prefer native image generation/editing and supported browser capabilities. Exact data charts and diagrams use deterministic tools. Map Claude-specific tool names and unavailable hooks to available equivalents.
- Preserve existing code and user decisions. Existing authorization covers routine reversible implementation and checks; ask only when a material input or decision is missing.
- Installing files does not activate external accounts or paid APIs. Check dependencies when needed, do not send data or spend API quota just to demonstrate skill discovery, and state which behavior was actually exercised.

## Save new reusable skills centrally

Store reusable source under the shared repository's `skills/<name>/` with all bundled resources and original license notices. Run its registry builder and validator, review same-name differences, and save only the task changes to the shared repository. Project-specific rules stay in the project's AGENTS.md. Do not copy a private user profile or credentials into the public library.

For ChatGPT account-level installation use the platform's personal-skills workflow. For standalone clients, use the shared repository's sync_skills.py with the appropriate --agent or --target. Never describe a scratch copy or an ordinary global CLI copy as a verified ChatGPT account install.

## Report accurately

Name the selected skills and the result relevant to the user's task. Distinguish source availability, client installation, and actual execution. Do not claim every external dependency works merely because its skill file can be read.
