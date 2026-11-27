---
name: deepseek-collab
description: "High-leverage dual-brain orchestration pattern for pairing Antigravity/Codex with DeepSeek ('与ds合作', '调用ds', '和ds思考', '用DeepSeek并发'). Never underestimate DeepSeek's 3D/math/texture/copy capability: reserve the main model (~20%) for spatial architecture, contracts, integration, and real visual inspection, while dispatching ~80% of parallel heavy procedural textures, 3D modules, GLSL shaders, splines, CSS, and copywriting to DeepSeek via automated retry verification."
---

# DeepSeek Collaboration Protocol (`与 DS 合作 · 双脑并发工程铁律`)

**Never underestimate DeepSeek.** Both `deepseek-chat` and `deepseek-reasoner` excel at dense procedural Python/NumPy/PIL texture synthesis, Three.js glTF mesh construction, GLSL shaders, spline/IK mathematics, CSS systems, and stylized Chinese/English copywriting—provided you give them **unambiguous spatial contracts, exact helper signatures, bounded module size, and automated verification**.

---

## 1. The 80 / 20 Division of Labor

### Delegate ~80% to DeepSeek (Parallel Threads)
1. **Procedural 2D PBR Textures & Panoramas (`deepseek-chat`):**
   - Multi-layer weathered wood parquet, honed veining marble, woven carpet relief & borders, Venetian Marmorino limewash plaster, architectural boiserie panels, linen/bouclé weaves, 4K equirectangular sunset/twilight sky domes, archival gallery paintings.
2. **Modular 3D Geometry Builders (`deepseek-chat`):**
   - Independent architectural rooms, bespoke furniture pieces, lamps, foliage, vessels, railings, docks, vessels conforming to an explicit shared `MeshBuilder` / `SceneContext` interface and world bounding box.
3. **3D Math, Shaders & Motion (`deepseek-reasoner`):**
   - C² camera spline trajectories, Gerstner water wave / sun-glitter GLSL shaders, buoyancy probes, room-envelope collision clamps, procedural wing/tail kinematics.
4. **Refined UI Styling & Multi-Tone Copy (`deepseek-chat`):**
   - Translucent HUD panels, channel OSDs, rich contextual character monologues & worldbuilding copy (checked against project forbidden-word lists).

### Reserve ~20% for Main Agent (High-Judgment Architect)
1. **Master Spatial Map & Interface Contracts:** Author shared coordinates, camera anchors, lighting mood targets, and exact function signatures.
2. **Core State Machine & API Wiring:** Keep sensitive game scoring, auth, and scene transitions deterministic and clean.
3. **Real-Browser Visual Inspection ("Open Eyes" QA):** Render in real Chromium across desktop & tablet viewports, read actual screenshots, catch backface winding bugs / height mismatches / sterile walls, and drive final polish.

---

## 2. Five Iron Rules for Reliable First-Pass DeepSeek Codegen

Review [references/prompt-contract-checklist.md](references/prompt-contract-checklist.md) before launching any batch:

1. **Paste Exact Signatures:** Always include exact parameter lists and method names of shared helpers (`SceneContext`, `MeshBuilder`, return types). Never let DeepSeek guess helper APIs.
2. **Lock Every Module Under ~260 Lines:** DeepSeek caps output at `8192` tokens per request. Split large builders cleanly by texture/furniture/architecture so zero files truncate mid-function.
3. **Enforce Outward Winding & Elevation Contracts:** Explicitly state `+Y` up, outward normal conventions for `add_quad` (`cross(p1-p0, p2-p0)`), exact floor/tabletop `Y` datums, and exact camera-facing axes.
4. **Embed Deterministic Visual Polish Rules:** Include domain-specific visual craftsmanship rules in the system prompt (e.g., *no blank flat walls—use architectural panels, reveals, tonal depth, and woven borders*).
5. **Pair Every Task With Automated Self-Healing (`verify_cmd`):** Run a zero-turn Python worker loop that executes syntax/AST checks, image dimension & color-variance assertions, triangle/AABB checks, and forbidden-word scans—feeding any stderr traceback back to DeepSeek for up to 3 automatic retries before bothering the main context.

---

## 3. Anti-Pattern Checklist (Do Not Do This)

- Hand-writing hundreds of lines of NumPy procedural texture noise or repetitive box/lathe coordinates in the main agent turn.
- Dispatching vague prompts ("make a luxury sofa and table") without X/Y/Z bounding boxes or shared surface datums (causes mismatched heights and floating props).
- Accepting a generated script without running both structural assertions and visually inspecting the rendered output in Chromium.
