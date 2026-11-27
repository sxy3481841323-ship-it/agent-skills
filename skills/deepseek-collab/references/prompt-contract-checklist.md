# DeepSeek Prompt & Verification Contract Checklist

Every DeepSeek task spec submitted to `ds_worker.py` (or equivalent orchestrator) should include:

1. **Exact Target Path & Line Budget**: e.g. `Target lines: 160–240` (strictly `< 280` to avoid `8192`-token truncation).
2. **Verbatim Helper Signatures**: Copy the exact `def` signatures of `MeshBuilder` / `SceneContext` / shared utils so DeepSeek never hallucinates keyword args.
3. **Exact World Coordinate & Datum Box**:
   - Floor datum `Y`, tabletop datum `Y`, sofa seat height `Y`, wall plane `X`/`Z`, inward facing direction (`-X`, `+Z`, `-Z`), and non-overlap clearances.
4. **Required Identifiers**: Exact mesh names (`mesh.name`) or export function names asserted by downstream scripts.
5. **Automated `verify_cmd`**:
   - Python: `python3 -m py_compile <file>` + lightweight import & smoke call checking output image dimensions / RGB std / mesh triangle counts / bounding boxes.
   - JS: `node --check <file>` + forbidden-term / CDN regex scan.
