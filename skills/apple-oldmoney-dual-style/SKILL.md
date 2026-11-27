---
name: apple-oldmoney-dual-style
description: "Dual-aesthetic UI & 3D spatial standard combining Old-Money architectural quiet luxury (tactile limewash/limestone boiserie, fluted walnut, Roman travertine, hand-knotted bordered silk-wool rugs, warm brass hardware—ZERO blank white walls) with Apple fluid minimalism (smoked/warm translucent vibrancy, tabular numerals, tactile spring feedback, clean typography, quiet hardware chrome). Use when designing or upgrading 3D interiors, foyers, HUDs, or flagship web apps that forbid generic white-box minimalism."
---

# Old-Money Architectural Craft × Apple Fluid Minimalism

This design system unites two complementary disciplines without contradiction:
- **Architectural & Material World (Physical Space / 3D):** **Old-Money Quiet Luxury** (Maxime d'Angeac, Axel Vervoordt, Loro Piana, Orient Express heritage interiors).
- **Digital Controls, Displays & HUD Chrome (Interface / 2D):** **Apple Fluid Minimalism** (translucent smoked-linen vibrancy, crisp typographic hierarchy, spring-damped interactions, calm restraint).

---

## 1. The Cardinal Ban: Blank White Walls Are NOT Minimalism

Empty `#FFFFFF` or flat off-white slabs read as unfinished contractor drywall, **not** minimal luxury. Even quiet walls require **material depth and architectural rhythm**:
- **Wall Finishes:** Use warm hand-troweled French Marmorino limewash / honed Roman limestone (`#DFD5C5`–`#CBBBA3`) with subtle mineral variation—never flat uniform cream/white.
- **Architectural Rhythm:** Divide long interior & foyer corridors with raised boiserie mouldings, fluted American walnut pilasters, brushed-bronze shadow-gap reveals (`4–8 mm` recessed dark bronze/brass lines), and backlit architectural niches.
- **Floor-to-Wall Transition:** Anchor floors with inlaid walnut/brass perimeter borders around herringbone French oak or honed stone pavers.

---

## 2. Carpet, Rug & Furniture Proportion Law

1. **Museum-Grade Bordered Rugs:** Never drop a flat solid rectangle under a sofa. Give salon and foyer rugs subtle silk *abrash* variation, a woven architectural multi-band border (taupe, antique brass, charcoal, with at most one muted heritage thread), and low physical relief.
2. **Conversational Reach & Datum Discipline:**
   - Staggered / non-aligned multi-table arrangements look curated and residential **only when sharing an intentional architectural height datum** (typically `top Y = 0.72–0.78 m` for lounge coffee tables—never arbitrary mismatched heights unless clearly tiered as a nesting end-table).
   - Keep the primary table edge within `0.15–0.45 m` of the nearest lounge seat / chaise so every seat feels served.
3. **Grounded Lighting Hardware:** Floor lamps beside sculpted speakers or reading chairs need architectural mass—heavy travertine or bronze plinths, solid fluted wood/brass shafts (`Ø >= 75 mm`), and tailored linen or alabaster shades—never hairline wireframe arcs.
4. **Curated Gallery Restraint:** Prefer **one monumental museum-lit masterwork** or a disciplined architectural diptych over a cluttered row of 4 small mismatched frames.

---

## 3. Window & Exterior Vista Law (AAA Multi-Layer Parallax)

Never stick a flat photo right behind a window glass pane:
1. Build a **foreground balcony/terrace deck** generous enough for full-scale lounge seating facing the view (`>= 10–14 m` deep for ocean cliff vistas).
2. Place **mid-ground 3D silhouettes** (coastal headlands, trees, moored craft) at distinct depth planes (`50–120 m`) for true parallax during 360° camera orbit.
3. Wrap the horizon with an **animated water / atmospheric sky dome** tuned to golden-hour warmth or twilight glow so exterior views feel inhabited and alive.

---

## 4. Apple Fluid Minimalism for HUD & In-World Displays

- **Surfaces:** Smoked warm glass (`rgba(20, 19, 18, 0.72)`, `backdrop-filter: blur(20px) saturate(160%)`) with crisp `1px solid rgba(226, 198, 138, 0.24)` hairlines—never heavy gradients or noisy neon cards.
- **Interaction Physics:** Instant tactile press (`transform: scale(0.97)`), smooth damped transitions (`cubic-bezier(0.22, 1, 0.36, 1)`), tabular numbers (`font-variant-numeric: tabular-nums`), and `@media (prefers-reduced-motion: reduce)` fallbacks.
- **No Blank Screens:** In-world displays (`TV`, concierges) default to tasteful quiet programming (live regatta, fine-art/horology auction previews, equestrian turf, candlelit chamber music) rather than dead black glass or stock placeholder noise.
