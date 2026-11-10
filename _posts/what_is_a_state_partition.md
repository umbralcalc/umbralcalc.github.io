---
title: "What is a state partition?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partitions.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-history.svg"
cites:
- "[[how_does_a_simulation_keep_track_of_time]]"
nocite: |
  @grimm2006, @durbinkoopman2012
---

# What is a state partition?
<div style="height:0.75em;"></div>

A state partition is one piece of a simulation's 'state'. Simulations have a 'state' associated to them for each value of time.

A simulation state holds all of the essential information we want to track to make the simulation useful to us which, crucially, includes _all of the information that is needed for the simulation to proceed_.

In order to simplify how all of this state data is processed and retrieved, we're going to _partition_ this simulation state into several 'state partition' data structures.

For example, one of these partitions might hold all the data associated to a player in a sports team, and the whole simulation needs all of the players within its overall state.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partitions.svg" width=600/></center>

Each state partition carries data that can be different for each moment in time of the simulation. In order to track this evolution, we create a 'state partition history' data structure for each state partition.

Each state partition history has indices which always match those of the cumulative timesteps history, so they are always synchronised with each other.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-history.svg" width=600/></center>

## Example: Energy usage in a smart building

```{=html}
<div id="sim-history-demo" style="margin:1.5em 0;padding:1em;background:#ffffff;">
  <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;margin-bottom:0.9em;">
    <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Overall time series (temperature)</div>
    <svg id="sim-history-overall" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Overall time series"></svg>
    <div style="font-size:1rem;color:#2c3e50;padding:0 0.75em;margin-bottom:0.35em;">Highlighted window corresponds to the history panels below.</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:0.9em;">
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Cumulative timesteps history</div>
      <svg id="sim-history-timeline" width="100%" height="140" viewBox="0 0 320 140" role="img" aria-label="Cumulative timesteps history"></svg>
      <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">The most recent time is at the top.</div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">State partition histories</div>
      <svg id="sim-history-partitions" width="100%" height="140" viewBox="0 0 320 140" role="img" aria-label="State partition histories"></svg>
      <div id="sim-history-state" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;margin-bottom:0.35em;"></div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.8em;">
    <button id="sim-history-step" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Advance 1 timestep
    </button>
    <button id="sim-history-reset" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      New simulation run
    </button>
  </div>
</div>
<script>
(() => {
  const overallSvg = document.getElementById("sim-history-overall");
  const timelineSvg = document.getElementById("sim-history-timeline");
  const partitionsSvg = document.getElementById("sim-history-partitions");
  const stepButton = document.getElementById("sim-history-step");
  const resetButton = document.getElementById("sim-history-reset");
  const stateBox = document.getElementById("sim-history-state");
  if (!overallSvg || !timelineSvg || !partitionsSvg || !stepButton || !resetButton) return;

  const width = 320;
  const height = 140;
  const pad = 18;
  const maxHistory = 8;
  const totalSteps = 24;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const makeState = () => ({
    time: 0,
    history: [],
    overall: [],
    occupancy: 4 + Math.floor(Math.random() * 6),
    temperature: 20 + Math.random() * 2.5,
  });

  let sim = makeState();

  const advance = () => {
    const delta = 1;
    sim.time += delta;
    const occupancyDrift = Math.random() < 0.5 ? -1 : 1;
    sim.occupancy = Math.max(0, sim.occupancy + occupancyDrift + (Math.random() < 0.3 ? 1 : 0));
    const targetTemp = 19 + sim.occupancy * 0.25;
    sim.temperature += (targetTemp - sim.temperature) * 0.3 + (Math.random() - 0.5) * 0.4;

    sim.history.unshift({
      time: sim.time,
      occupancy: sim.occupancy,
      temperature: sim.temperature,
    });
    if (sim.history.length > maxHistory) {
      sim.history.pop();
    }
    sim.overall.push({
      time: sim.time,
      occupancy: sim.occupancy,
      temperature: sim.temperature,
    });
    if (sim.overall.length > totalSteps) {
      sim.overall.shift();
    }
  };

  const drawOverall = () => {
    overallSvg.innerHTML = "";
    const chartPad = 16;
    const innerWidth = width - 2 * chartPad;
    const innerHeight = height - 2 * chartPad;
    const temps = sim.overall.map((entry) => entry.temperature);
    const minTemp = Math.min(...temps);
    const maxTemp = Math.max(...temps);
    const range = maxTemp - minTemp || 1;

    overallSvg.appendChild(createSvgEl("rect", {
      x: chartPad,
      y: chartPad,
      width: innerWidth,
      height: innerHeight,
      fill: "#ffffff",
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    const points = sim.overall.map((entry, idx) => {
      const x = chartPad + (idx / (totalSteps - 1)) * innerWidth;
      const y = chartPad + innerHeight - ((entry.temperature - minTemp) / range) * innerHeight;
      return { x, y };
    });

    if (points.length > 1) {
      const path = points.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
      overallSvg.appendChild(createSvgEl("path", {
        d: path,
        fill: "none",
        stroke: "#3c78d8",
        "stroke-width": "2",
      }));
    }

    points.forEach((point, idx) => {
      overallSvg.appendChild(createSvgEl("circle", {
        cx: point.x,
        cy: point.y,
        r: idx === points.length - 1 ? 3.5 : 2,
        fill: "#2c3e50",
      }));
    });

    const windowStart = Math.max(0, sim.overall.length - maxHistory);
    const windowX = chartPad + (windowStart / (totalSteps - 1)) * innerWidth;
    const windowWidth = ((sim.overall.length - windowStart - 1) / (totalSteps - 1)) * innerWidth;
    overallSvg.appendChild(createSvgEl("rect", {
      x: windowX,
      y: chartPad,
      width: Math.max(8, windowWidth),
      height: innerHeight,
      fill: "rgba(176,68,122,0.12)",
      stroke: "#b0447a",
      "stroke-width": "1",
      "stroke-dasharray": "4 3",
    }));
  };

  const drawTimeline = () => {
    timelineSvg.innerHTML = "";
    const rowHeight = (height - 2 * pad) / maxHistory;
    const startX = pad + 12;

    timelineSvg.appendChild(createSvgEl("line", {
      x1: startX,
      y1: pad,
      x2: startX,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    sim.history.forEach((entry, idx) => {
      const y = pad + rowHeight * idx + rowHeight / 2;
      timelineSvg.appendChild(createSvgEl("circle", {
        cx: startX,
        cy: y,
        r: 4,
        fill: idx === 0 ? "#b0447a" : "#2c3e50",
      }));
      timelineSvg.appendChild(createSvgEl("text", {
        x: startX + 12,
        y: y + 4,
        fill: "#2c3e50",
        "font-size": "11",
      })).textContent = `t = ${entry.time}`;
    });
  };

  const drawPartitions = () => {
    partitionsSvg.innerHTML = "";
    const rowHeight = (height - 2 * pad) / maxHistory;
    const startX = pad + 8;

    const minOcc = Math.min(...sim.history.map((h) => h.occupancy));
    const maxOcc = Math.max(...sim.history.map((h) => h.occupancy));
    const minTemp = Math.min(...sim.history.map((h) => h.temperature));
    const maxTemp = Math.max(...sim.history.map((h) => h.temperature));

    sim.history.forEach((entry, idx) => {
      const y = pad + rowHeight * idx + rowHeight / 2;
      const occWidth = maxOcc === minOcc ? 0.5 : (entry.occupancy - minOcc) / (maxOcc - minOcc);
      const tempWidth = maxTemp === minTemp ? 0.5 : (entry.temperature - minTemp) / (maxTemp - minTemp);

      partitionsSvg.appendChild(createSvgEl("rect", {
        x: startX,
        y: y - 8,
        width: 70 * occWidth + 10,
        height: 6,
        fill: "#b0447a",
        rx: "2",
      }));
      partitionsSvg.appendChild(createSvgEl("rect", {
        x: startX,
        y: y + 2,
        width: 70 * tempWidth + 10,
        height: 6,
        fill: "#3c78d8",
        rx: "2",
      }));

      partitionsSvg.appendChild(createSvgEl("text", {
        x: startX + 90,
        y: y + 4,
        fill: "#2c3e50",
        "font-size": "11",
      })).textContent = `occ ${entry.occupancy} | temp ${entry.temperature.toFixed(1)}°C`;
    });

  };

  const render = () => {
    if (sim.history.length === 0) {
      for (let i = 0; i < totalSteps; i += 1) {
        advance();
      }
    }
    drawOverall();
    drawTimeline();
    drawPartitions();
    if (stateBox && sim.history[0]) {
      const latest = sim.history[0];
      stateBox.innerHTML = `
        <div><strong>Latest simulation state:</strong> occupancy ${latest.occupancy}, temperature ${latest.temperature.toFixed(1)}°C.</div>
        <div>Both histories are indexed by the same times.</div>
      `;
    }
  };

  stepButton.addEventListener("click", () => {
    advance();
    render();
  });

  resetButton.addEventListener("click", () => {
    sim = makeState();
    render();
  });

  render();
})();
</script>
```

## References and further reading

::: {#refs}
:::
