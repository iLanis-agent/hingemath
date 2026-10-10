#!/usr/bin/env python3
"""Oracle mirror of engine.js for Hinge math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def hingeCount(doorKg, doorCm):
    if not (doorKg > 0) or not (doorCm > 0):
        return {"error": "door weight and height must be positive"}
    if doorKg <= 18: count = 2
    elif doorKg <= 40: count = 3
    elif doorKg <= 60: count = 4
    else: count = 5
    bumped = False
    if doorCm > 230 and count < 5:
        count += 1; bumped = True
    return {"doorKg": jsnum(float(doorKg)), "doorCm": jsnum(float(doorCm)), "hinges": count, "heightBump": bumped}

def hingePlace(doorCm, count):
    if not (doorCm > 0):
        return {"error": "door height must be positive"}
    if count != math.floor(count + 0.5) or count < 2:
        return {"error": "hinge count must be a whole number of at least 2"}
    if doorCm <= 46:
        return {"error": "door height must clear the labeled 18 and 28 cm offsets"}
    top = 18; bottom = doorCm - 28
    positions = [jsnum(r1(top + i * (bottom - top) / (count - 1))) for i in range(count)]
    return {"doorCm": jsnum(float(doorCm)), "hinges": count, "positions": positions}

def screwPlan(hinges, perHinge, packSize):
    if not (hinges > 0) or not (perHinge > 0) or not (packSize > 0):
        return {"error": "all screw inputs must be positive"}
    if hinges != math.floor(hinges + 0.5):
        return {"error": "hinge count must be a whole number"}
    total = hinges * perHinge
    packs = math.ceil(total / packSize)
    return {"hinges": jsnum(float(hinges)), "perHinge": jsnum(float(perHinge)), "packSize": jsnum(float(packSize)),
            "total": jsnum(float(total)), "packs": packs, "spare": jsnum(float(packs * packSize - total))}

def renderCount(r):
    return ("A " + fmt(r["doorKg"]) + " kg door " + fmt(r["doorCm"]) + " cm tall takes " + str(r["hinges"]) +
            " hinges on the labeled weight bands" +
            (" - one extra because the door is over the labeled 230 cm line" if r["heightBump"] else "") + ".")

def renderPlace(r):
    return ("On a " + fmt(r["doorCm"]) + " cm door, " + str(r["hinges"]) + " hinges sit " +
            ", ".join(fmt(p) for p in r["positions"]) +
            " cm from the top (labeled 18 cm down and 28 cm up, middles spread evenly).")

def renderScrews(r):
    return (str(r["hinges"]) + " hinges at a labeled " + fmt(r["perHinge"]) + " screws each is " + fmt(r["total"]) +
            " screws - " + str(r["packs"]) + " pack" + ("" if r["packs"] == 1 else "s") + " of " + fmt(r["packSize"]) +
            ", " + fmt(r["spare"]) + " spare.")

CASES = []
def add(fn, args): CASES.append({"fn": fn, "args": args})

for a in [(12, 204), (25, 204), (18, 204), (40, 204), (45, 204), (60, 204), (75, 204), (25, 240), (12, 235), (70, 235), (0, 204), (25, 0)]:
    add("hingeCount", list(a))
for a in [(204, 3), (204, 2), (204, 5), (100, 2), (46.5, 2), (240, 4), (204, 2.5), (204, 1), (46, 2), (0, 3), (204, 0), (210, 3)]:
    add("hingePlace", list(a))
for a in [(3, 8, 25), (2, 8, 25), (5, 8, 25), (4, 6, 20), (3, 8, 24), (6, 10, 50), (0, 8, 25), (2.5, 8, 25), (3, 0, 25), (3, 8, 0), (1, 8, 25)]:
    add("screwPlan", list(a))

out = []
for c in CASES:
    fn = {"hingeCount": hingeCount, "hingePlace": hingePlace, "screwPlan": screwPlan}[c["fn"]]
    res = fn(*c["args"])
    is_err = "error" in res
    if is_err:
        render = res["error"]
    else:
        render = {"hingeCount": renderCount, "hingePlace": renderPlace, "screwPlan": renderScrews}[c["fn"]](res)
    out.append({"fn": c["fn"], "args": c["args"], "result": res, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
print("wrote", len(out), "cases")
