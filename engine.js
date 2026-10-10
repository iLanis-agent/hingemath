/* Hinge math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }

  function hingeCount(doorKg, doorCm) {
    if (!(doorKg > 0) || !(doorCm > 0)) return { error: "door weight and height must be positive" };
    var count;
    if (doorKg <= 18) count = 2;
    else if (doorKg <= 40) count = 3;
    else if (doorKg <= 60) count = 4;
    else count = 5;
    var bumped = false;
    if (doorCm > 230 && count < 5) { count = count + 1; bumped = true; }
    return { doorKg: doorKg, doorCm: doorCm, hinges: count, heightBump: bumped };
  }

  function hingePlace(doorCm, count) {
    if (!(doorCm > 0)) return { error: "door height must be positive" };
    if (count !== Math.round(count) || count < 2) return { error: "hinge count must be a whole number of at least 2" };
    if (doorCm <= 46) return { error: "door height must clear the labeled 18 and 28 cm offsets" };
    var positions = [];
    var top = 18, bottom = doorCm - 28;
    for (var i = 0; i < count; i++) {
      positions.push(r1(top + i * (bottom - top) / (count - 1)));
    }
    return { doorCm: doorCm, hinges: count, positions: positions };
  }

  function screwPlan(hinges, perHinge, packSize) {
    if (!(hinges > 0) || !(perHinge > 0) || !(packSize > 0)) return { error: "all screw inputs must be positive" };
    if (hinges !== Math.round(hinges)) return { error: "hinge count must be a whole number" };
    var total = hinges * perHinge;
    var packs = Math.ceil(total / packSize);
    return { hinges: hinges, perHinge: perHinge, packSize: packSize, total: total, packs: packs, spare: packs * packSize - total };
  }

  function renderCount(r) {
    return "A " + r.doorKg + " kg door " + r.doorCm + " cm tall takes " + r.hinges + " hinges on the labeled weight bands" + (r.heightBump ? " - one extra because the door is over the labeled 230 cm line" : "") + ".";
  }

  function renderPlace(r) {
    return "On a " + r.doorCm + " cm door, " + r.hinges + " hinges sit " + r.positions.join(", ") + " cm from the top (labeled 18 cm down and 28 cm up, middles spread evenly).";
  }

  function renderScrews(r) {
    return r.hinges + " hinges at a labeled " + r.perHinge + " screws each is " + r.total + " screws - " + r.packs + " pack" + (r.packs === 1 ? "" : "s") + " of " + r.packSize + ", " + r.spare + " spare.";
  }

  var api = { hingeCount: hingeCount, hingePlace: hingePlace, screwPlan: screwPlan, renderCount: renderCount, renderPlace: renderPlace, renderScrews: renderScrews };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.HingeMath = api;
})(typeof window !== "undefined" ? window : this);
