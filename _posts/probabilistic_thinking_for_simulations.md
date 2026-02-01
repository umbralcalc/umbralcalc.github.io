---
title: "Probabilistic thinking for simulations"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
order: 5
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition-region.svg"
---

# Probabilistic thinking for simulations
<div style="height:0.75em;"></div>

## Why do we care about probabilities?

The 'Trajectory' of a simulation is the sequence of possible State Values that its Partitions actually take during a specific Simulation Run.

Probabilities can represent sampling all of the possible Trajectories that a simulation could take in Time, simultaneously.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg" /></center>

Using this representation for a real-world simulation, there are two important use cases.

The first uses all of the possible Trajectories the simulation can take to represent how likely it is to take them. This makes it possible to create algorithms which learn the most likely Parameters for State Partitions to match real-world Data.

The second uses the Probabilities to represent a model in place of the simulation itself. In the right circumstances, this results in algorithms which are much more efficient than sampling multiple Trajectories explicitly.

## Probabilities and regions

Evaluating the Probability of a particular State Partition History, given Parameters and a Cumulative Timesteps History, looks a similar to the Iterate computation. However, in contrast, this computation does _not_ progress forward in Time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition.svg" /></center>

We might also want to evaluate the Probability of Regions which join together possible values that the whole State Partition History can take.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/possible-region.svg" /></center>

In many situations, it would be impossible to count the all of the possible values in some Regions, but we can still imagine the computation in this way.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition-region.svg" /></center>

## Conditional probabilities

We can relate two successive probability evaluations in Time together by making the answer of the second depend on the outcome of the first.

We call the second of these two evaluations a Conditional Probability because its Probability is _conditional_ on the Probability of the first.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/conditional-probability.svg" /></center>

The Probabilities for the whole State Partition History change as the simulation advances in Time by adding the Next State Partition Values into the History.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evolving-state-partition-history-probability.svg" /></center>

This concept also applies to the Probability of Regions.

Note how this relationship also describes how the Probabilities of State Partition Histories can evolve in Time. One applies the same calculation to the output from the previous one, and so on, recursively.

So why can’t we just use this recursive relationship to model all the trajectories of the simulation at once? For some simpler systems this is indeed possible, but for most simulations in practice this is computationally infeasible.

Think about how one might store the set of all Possible State Partition Histories for a sequence of coin flips, and then how this can proliferate in Time as the simulation advances.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/coin-flips-tree.svg" /></center>

The Possible State Partition Histories grow even though the Possible State Values of a coin flip always remain the same (Heads or Tails).

## Example: Randomly moving point in 2 dimensions

In practice, for most real-world systems, the set of Possible State Values _also_ grows. To see how this can be the case, consider the Trajectories of a randomly moving point on a simple 2-dimensional grid.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/random-walker-grid.svg" /></center>

```{=html}
<div id="random-walker-demo" style="margin:1.3em 0 0.5em;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Random moving point (visited State Values)</div>
  <svg id="random-walker-svg" width="100%" height="200" viewBox="0 0 320 200" role="img" aria-label="Random walker lattice"></svg>
  <div id="random-walker-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;">
  <button id="random-walker-step" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    Advance 10 Timesteps
  </button>
  <button id="random-walker-reset" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    Reset simulation
  </button>
</div>
<script>
(() => {
  const svg = document.getElementById("random-walker-svg");
  const stepBtn = document.getElementById("random-walker-step");
  const resetBtn = document.getElementById("random-walker-reset");
  const text = document.getElementById("random-walker-text");
  if (!svg || !stepBtn || !resetBtn || !text) return;

  const width = 320;
  const height = 200;
  const gridSize = 9;
  const cell = 18;
  const padX = (width - gridSize * cell) / 2;
  const padY = (height - gridSize * cell) / 2;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  let walker = { x: Math.floor(gridSize / 2), y: Math.floor(gridSize / 2) };
  let visits = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));
  visits[walker.y][walker.x] = 1;
  let steps = 0;

  const step = () => {
    const moves = [
      { x: 1, y: 0 },
      { x: -1, y: 0 },
      { x: 0, y: 1 },
      { x: 0, y: -1 },
    ];
    const move = moves[Math.floor(Math.random() * moves.length)];
    walker.x = Math.max(0, Math.min(gridSize - 1, walker.x + move.x));
    walker.y = Math.max(0, Math.min(gridSize - 1, walker.y + move.y));
    visits[walker.y][walker.x] += 1;
    steps += 1;
  };

  const render = () => {
    svg.innerHTML = "";
    const maxVisit = Math.max(...visits.flat());

    for (let y = 0; y < gridSize; y += 1) {
      for (let x = 0; x < gridSize; x += 1) {
        const intensity = visits[y][x] / maxVisit;
        const color = intensity === 0
          ? "#ffffff"
          : `rgba(176, 68, 122, ${0.15 + 0.6 * intensity})`;
        svg.appendChild(createSvgEl("rect", {
          x: padX + x * cell,
          y: padY + y * cell,
          width: cell - 1,
          height: cell - 1,
          fill: color,
          stroke: "#2c3e50",
          "stroke-width": "0.5",
        }));
      }
    }

    svg.appendChild(createSvgEl("rect", {
      x: padX + walker.x * cell,
      y: padY + walker.y * cell,
      width: cell - 1,
      height: cell - 1,
      fill: "rgba(60, 120, 216, 0.5)",
      stroke: "#3c78d8",
      "stroke-width": "1",
    }));

    text.innerHTML = `
      <div><strong>Steps:</strong> ${steps}. Darker squares mean higher visit count.</div>
      <div>The set of possible State Values grows as the point moves over the grid.</div>
    `;
  };

  stepBtn.addEventListener("click", () => {
    for (let i = 0; i < 10; i += 1) {
      step();
    }
    render();
  });

  resetBtn.addEventListener("click", () => {
    walker = { x: Math.floor(gridSize / 2), y: Math.floor(gridSize / 2) };
    visits = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));
    visits[walker.y][walker.x] = 1;
    steps = 0;
    render();
  });

  render();
})();
</script>
```

## Estimating the statistics of state values

There is a way we can compute these Probabilities without having to trace the path of every possible Trajectory, and often without having to keep a record of every Possible State Value.

We start by estimating the Statistics of these Probabilities. 

The simplest example of these Statistics is the Estimated Mean State Value. 

The obvious way to calculate this is to take the average State Value for a given Timestep across multiple simulation Trajectories.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/average-across-trajectories.svg" /></center>

But could we get an estimate of Statistics from only one Trajectory to avoid all the additional computations?

## Example: Estimating with a weighted average

Yes! If we have an accurate 'weighting model' for the past values, we can get an Estimated Mean State Value from a weighted average over the full State Partition History.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/weighted-average.svg" /></center>

```{=html}
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.9em;">
  <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
    <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Many Trajectories</div>
    <svg id="many-traj-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Many trajectories"></svg>
    <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Average across multiple Simulation Runs.</div>
  </div>
  <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
    <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Weighted State Partition History</div>
    <svg id="weighted-traj-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Weighted trajectory"></svg>
    <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">One Trajectory with recency weights.</div>
  </div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.5em;margin-bottom:1em;">
  <button id="weighted-traj-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    Resample Trajectories
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

We might also train a Machine Learning model to predict the Statistics of State Values from the full State Partition History as an alternative.

Note that there are situations where using the State Partition Histories from one Trajectory is not equivalent to using multiple Trajectories (see [Ergodicity](https://en.wikipedia.org/wiki/Ergodicity)). But this kind of technical problem can often be mitigated by using some mix of the two methods.

## Estimating the probabilities of state values

So we have the Statistics, but where have the Probabilities gone?

There are many different types of mathematical formulae or Machine Learning model which can provide a map back from these estimated Statistics into Probabilities of State Values in Time for either one or multiple Trajectories, depending on the right circumstances.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/distributions.svg" /></center>

Using calculations of the estimated Statistics for a single Trajectory from the State Partition History, we can design a 'Probabilistic Sample Weighting' algorithm using the [stochadex simulation engine](https://umbralcalc.github.io/stochadex) we introduced in a previous post.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/prob-reweighting-code.svg" /></center>

This algorithm essentially compresses the information held within the State Partition History into a small amount of data in the form of Statistics. It then uses these Statistics to calculate estimated Probabilities for any Possible State Value in Time.
