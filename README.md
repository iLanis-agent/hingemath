# Hinge math

How many hinges a door takes, where they sit on the stile, and how many screws and packs to buy. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/hingemath/

## The three tools

- **Hinge count** - `hingeCount(doorKg, doorCm)`: labeled weight bands (2 up to 18 kg, 3 up to 40, 4 up to 60, 5 above), plus one extra for doors over 230 cm, capped at 5.
- **Hinge placement** - `hingePlace(doorCm, count)`: labeled 18 cm from the top and 28 cm from the bottom, middles spread evenly, positions to 0.1 cm.
- **Screw plan** - `screwPlan(hinges, perHinge, packSize)`: total screws, packs to buy, spares left over.

## Labeled norms (illustrative references, not rules)

- Weight bands: up to 18 kg takes 2 hinges, up to 40 kg takes 3, up to 60 kg takes 4, heavier takes 5.
- Tall-door norm: over 230 cm earns one extra hinge, up to 5.
- Placement offsets: 18 cm from the top, 28 cm from the bottom.
- Screw typical: 8 per hinge (4 per leaf).

Heavy, exterior or fire-rated doors follow their own hardware schedules.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (35 cases, 105 checks)

Regenerate the oracle expectations: `python3 oracle.py`
