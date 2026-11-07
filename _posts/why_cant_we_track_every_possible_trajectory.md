---
title: Why can't we track every possible trajectory?
tag: How can I simulate the real world?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/coin-flips-tree.svg
aliases:
  - Why can't we track every possible trajectory?
cites:
  - "[[what_is_a_conditional_probability_in_a_simulation]]"
  - "[[how_can_i_simulate_the_real_world_introduction]]"
nocite: |
  @owen2013, @chopin2020
---

# Why can't we track every possible trajectory?
<div style="height:0.75em;"></div>

So why can’t we just use this recursive relationship to model all the trajectories of the simulation at once? For some simpler systems this is indeed possible, but for most simulations in practice this is computationally infeasible.

Think about how one might store the set of all possible state partition histories for a sequence of coin flips, and then how this can proliferate in time as the simulation advances.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/coin-flips-tree.svg" /></center>

The possible state partition histories grow even though the possible state values of a coin flip always remain the same (heads or tails).

## Example: Randomly moving point in 2 dimensions

In practice, for most real-world systems, the set of possible state values _also_ grows. To see how this can be the case, consider the trajectories of a randomly moving point on a simple 2-dimensional grid.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/random-walker-grid.svg" /></center>

```{=html}
<div id="random-walker-demo" style="margin:1.3em 0 0.5em;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Random moving point (visited state values)</div>
  <svg id="random-walker-svg" width="100%" height="200" viewBox="0 0 320 200" role="img" aria-label="Random walker lattice"></svg>
  <div id="random-walker-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;">
  <button id="random-walker-step" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    Advance 3 timesteps
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
      <div>The set of state values the simulation could have visited grows quickly with every step.</div>
    `;
  };

  stepBtn.addEventListener("click", () => {
    for (let i = 0; i < 3; i += 1) {
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

## References and further reading

::: {#refs}
:::
