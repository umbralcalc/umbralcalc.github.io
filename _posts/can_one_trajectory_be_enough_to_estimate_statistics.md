---
title: "Can one trajectory be enough to estimate statistics?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/weighted-average.svg"
cites:
- "[[how_can_i_simulate_the_real_world]]"
- "[[how_do_we_estimate_statistics_across_trajectories]]"
nocite: |
  @doucet2011, @gordon1993
---

# Can one trajectory be enough to estimate statistics?
<div style="height:0.75em;"></div>

Yes! If we have an accurate 'weighting model' for the past values, we can get an estimated mean state value from a weighted average over the full state partition history.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/weighted-average.svg" /></center>

```{=html}
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.9em;">
  <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
    <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Many trajectories</div>
    <svg id="many-traj-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Many trajectories"></svg>
    <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Average across multiple simulation runs.</div>
  </div>
  <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
    <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Weighted state partition history</div>
    <svg id="weighted-traj-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Weighted trajectory"></svg>
    <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">One trajectory with recency weights.</div>
  </div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.5em;margin-bottom:1em;">
  <button id="weighted-traj-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    Resample trajectories
  </button>
</div>
<script>
(() => {
  const manySvg = document.getElementById("many-traj-svg");
  const weightedSvg = document.getElementById("weighted-traj-svg");
  const btn = document.getElementById("weighted-traj-btn");
  if (!manySvg || !weightedSvg || !btn) return;

  const width = 320;
  const height = 160;
  const pad = 16;
  const steps = 50;
  const runs = 20;

  const randn = () => {
    let u = 0;
    let v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const randomWalk = () => {
    const values = [0];
    for (let i = 1; i <= steps; i += 1) {
      values.push(values[i - 1] + randn() * 0.35);
    }
    return values;
  };

  const mapPoints = (values, minVal, maxVal) => values.map((value, idx) => {
    const x = pad + (idx / steps) * (width - 2 * pad);
    const y = height - pad - ((value - minVal) / (maxVal - minVal || 1)) * (height - 2 * pad);
    return { x, y };
  });

  const drawLine = (svg, points, color, widthPx, dash) => {
    if (points.length < 2) return;
    const path = points.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
    svg.appendChild(createSvgEl("path", {
      d: path,
      fill: "none",
      stroke: color,
      "stroke-width": widthPx,
      "stroke-dasharray": dash || "none",
    }));
  };

  const render = () => {
    const trajectories = Array.from({ length: runs }, () => randomWalk());
    const mean = Array.from({ length: steps + 1 }, (_, idx) =>
      trajectories.reduce((sum, traj) => sum + traj[idx], 0) / runs
    );

    const weightedPath = randomWalk();
    const weights = Array.from({ length: steps + 1 }, (_, idx) => Math.exp(-0.08 * (steps - idx)));
    const weightedMean = weights.reduce((sum, w, idx) => sum + w * weightedPath[idx], 0) / weights.reduce((a, b) => a + b, 0);

    const minVal = Math.min(
      ...trajectories.flat(),
      ...weightedPath
    );
    const maxVal = Math.max(
      ...trajectories.flat(),
      ...weightedPath
    );

    manySvg.innerHTML = "";
    weightedSvg.innerHTML = "";

    trajectories.forEach((traj) => {
      drawLine(manySvg, mapPoints(traj, minVal, maxVal), "rgba(60,120,216,0.18)", 1);
    });
    drawLine(manySvg, mapPoints(mean, minVal, maxVal), "#2c3e50", 2);

    drawLine(weightedSvg, mapPoints(weightedPath, minVal, maxVal), "#3c78d8", 2);
    const weightedLine = mapPoints(Array(steps + 1).fill(weightedMean), minVal, maxVal);
    drawLine(weightedSvg, weightedLine, "#b0447a", 2, "4 3");
  };

  btn.addEventListener("click", render);
  render();
})();
</script>
```

We might also train a machine learning model to predict the statistics of state values from the full state partition history as an alternative.

Note that there are situations where using the state partition histories from one trajectory is not equivalent to using multiple trajectories (see [ergodicity](#ref-wiki_ergodicity)). But this kind of technical problem can often be mitigated by using some mix of the two methods.

## References and further reading

::: {#refs}
:::
