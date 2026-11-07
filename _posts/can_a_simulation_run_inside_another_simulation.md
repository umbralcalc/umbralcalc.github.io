---
title: "Can a simulation run inside another simulation?"
tag: "How can I simulate the real world?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-simulation-run.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-sim-iterate.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-sim-from-history.svg"
aliases:
- "Can a simulation run inside another simulation?"
cites:
- "[[what_is_a_simulation_run]]"
- "[[how_do_state_partitions_share_information]]"
- "[[how_can_i_simulate_the_real_world_introduction]]"
nocite: |
  @sarkka2013
---

# Can a simulation run inside another simulation?
<div style="height:0.75em;"></div>

Enabling whole 'inner' simulation runs to start and complete within each timestep of an 'outer' simulation run is a very useful, and somewhat fundamental, building block for simulations in practice. We shall call these 'embedded simulation runs'.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-simulation-run.svg"/></center>

There are then several ways one can think of to pass information from the outer simulation into the inner simulation prior to running it on each timestep.

Treating the inner simulation as a partition of the outer simulation, one example is to simply pass parameters from the outer simulation into the inner simulation, and nothing else.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-sim-iterate.svg" width=600/></center>

Another example is to pass both the cumulative timesteps history and state partition histories from the outer simulation into the inner simulation, in addition to the parameters.

Consider how this might be used to create useful statistical operations over the history of the outer simulation, e.g., like rolling window averages.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-sim-from-history.svg" width=600/></center>

## Example: Rolling future temperature forecast

```{=html}
<div id="embedded-run-demo" style="margin:1.5em 0;padding:1em;background:#ffffff;">
  <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
    <svg id="embedded-run-chart" width="100%" height="180" viewBox="0 0 320 180" role="img" aria-label="Rolling temperature forecast"></svg>
    <div id="embedded-run-state" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;margin-bottom:0.35em;"></div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.8em;">
    <button id="embedded-run-step" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Advance outer simulation
    </button>
    <button id="embedded-run-reset" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      New outer simulation run
    </button>
  </div>
</div>
<script>
(() => {
  const chartSvg = document.getElementById("embedded-run-chart");
  const stepButton = document.getElementById("embedded-run-step");
  const resetButton = document.getElementById("embedded-run-reset");
  const stateBox = document.getElementById("embedded-run-state");
  if (!chartSvg || !stepButton || !resetButton) return;

  const width = 320;
  const height = 180;
  const pad = 18;
  const horizon = 6;
  const maxHistory = 18;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const makeState = () => ({
    time: 0,
    history: [],
    occupancy: 3 + Math.floor(Math.random() * 6),
    temperature: 20 + Math.random() * 2,
  });

  let sim = makeState();

  const advanceOuter = () => {
    sim.time += 1;
    sim.occupancy = Math.max(0, sim.occupancy + (Math.random() < 0.55 ? 1 : -1));
    const targetTemp = 19 + sim.occupancy * 0.3;
    sim.temperature += (targetTemp - sim.temperature) * 0.35 + (Math.random() - 0.5) * 0.4;
    sim.history.push({
      time: sim.time,
      occupancy: sim.occupancy,
      temperature: sim.temperature,
    });
    if (sim.history.length > maxHistory) {
      sim.history.shift();
    }
  };

  const runEmbeddedForecast = () => {
    const forecast = [];
    let temp = sim.temperature;
    let occ = sim.occupancy;
    for (let i = 0; i < horizon; i += 1) {
      occ = Math.max(0, occ + (Math.random() < 0.5 ? 1 : -1));
      const target = 19 + occ * 0.3;
      temp += (target - temp) * 0.35 + (Math.random() - 0.5) * 0.4;
      forecast.push(temp);
    }
    return forecast;
  };

  const mapPoints = (values, minVal, maxVal, startIndex = 0) => {
    const range = maxVal - minVal || 1;
    return values.map((value, idx) => {
      const t = startIndex + idx;
      const x = pad + (t / (maxHistory + horizon - 1)) * (width - 2 * pad);
      const y = height - pad - ((value - minVal) / range) * (height - 2 * pad);
      return { x, y };
    });
  };

  const drawLine = (svg, points, color, dash) => {
    if (points.length < 2) return;
    const path = points.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
    svg.appendChild(createSvgEl("path", {
      d: path,
      fill: "none",
      stroke: color,
      "stroke-width": "2",
      "stroke-dasharray": dash || "none",
    }));
  };

  const render = () => {
    if (sim.history.length === 0) {
      for (let i = 0; i < 6; i += 1) {
        advanceOuter();
      }
    }

    const forecast = runEmbeddedForecast();
    const pastTemps = sim.history.map((entry) => entry.temperature);
    const series = pastTemps.concat(forecast);
    const minVal = Math.min(...series);
    const maxVal = Math.max(...series);

    chartSvg.innerHTML = "";
    chartSvg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: height - pad,
      x2: width - pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));
    chartSvg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: pad,
      x2: pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    const pastPoints = mapPoints(pastTemps, minVal, maxVal, 0);
    const forecastPoints = mapPoints([sim.temperature].concat(forecast), minVal, maxVal, pastTemps.length - 1);
    drawLine(chartSvg, pastPoints, "#2c3e50");
    drawLine(chartSvg, forecastPoints, "#3c78d8", "5 4");

    const currentX = pad + ((pastTemps.length - 1) / (maxHistory + horizon - 1)) * (width - 2 * pad);
    chartSvg.appendChild(createSvgEl("line", {
      x1: currentX,
      y1: pad,
      x2: currentX,
      y2: height - pad,
      stroke: "#b0447a",
      "stroke-width": "1",
      "stroke-dasharray": "3 3",
    }));

    chartSvg.appendChild(createSvgEl("circle", {
      cx: pastPoints[pastPoints.length - 1].x,
      cy: pastPoints[pastPoints.length - 1].y,
      r: 3,
      fill: "#b0447a",
    }));

    const startPoint = pastPoints[pastPoints.length - 1];
    const endPoint = forecastPoints[forecastPoints.length - 1];
    const axisY = height - pad;
    const arrowY = axisY;
    chartSvg.appendChild(createSvgEl("line", {
      x1: startPoint.x,
      y1: arrowY,
      x2: endPoint.x,
      y2: arrowY,
      stroke: "#b0447a",
      "stroke-width": "1.5",
    }));

    const arrowSize = 6;
    chartSvg.appendChild(createSvgEl("polygon", {
      points: `${endPoint.x},${arrowY} ${endPoint.x - arrowSize},${arrowY - 4} ${endPoint.x - arrowSize},${arrowY + 4}`,
      fill: "#b0447a",
    }));

    const labelX = Math.min(endPoint.x - 6, startPoint.x + 8);
    chartSvg.appendChild(createSvgEl("text", {
      x: labelX,
      y: axisY + 14,
      fill: "#b0447a",
      "font-size": "10",
      "text-anchor": "start",
    })).textContent = "Embedded simulation run";

    if (stateBox) {
      stateBox.innerHTML = `
        <div><strong>Outer simulation state:</strong> t=${sim.time}, occupancy ${sim.occupancy}, temperature ${sim.temperature.toFixed(1)}°C.</div>
        <div><strong>Embedded simulation run:</strong> forecast ${horizon} timesteps ahead from the current state.</div>
      `;
    }
  };

  stepButton.addEventListener("click", () => {
    advanceOuter();
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
