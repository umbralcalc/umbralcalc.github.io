---
title: "The building blocks of simulations"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
order: 2
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/cumulative-timesteps-history.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partitions.svg"
---

# The building blocks of simulations
<div style="height:0.75em;"></div>

## Time and its 'history'

Time is probably the most important variable to track in a simulation. This is because everything that happens within a simulation only has meaning with respect to the real world if we can trace what point in simulated Time that it happened.

Time is a variable in the simulation which always increases in value. We often want to track how it increases after each discrete simulation 'step' in increments which we shall call 'Timesteps'.

The first data structure which we shall introduce here is a 'Cumulative Timesteps History', which indexes simulated Times that the simulation _had_ according to _decreasing recency_.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/cumulative-timesteps-history.svg" width=600/></center>

## State partitions and their history

Simulations also have a 'State' associated to them for each value of Time.

A simulation State holds all of the essential information we want to track to make the simulation useful to us which, crucially, includes _all of the information that is needed for the simulation to proceed_.

In order to simplify how all of this State data is processed and retrieved, we're going to _partition_ this simulation State into several 'State Partition' data structures.

For example, one of these partitions might hold all the data associated to a player in a sports team, and the whole simulation needs all of the players within its overall State.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partitions.svg" width=600/></center>

Each State Partition carries data that can be different for each moment in Time of the simulation. In order to track this evolution, we create a 'State Partition History' data structure for each State Partition.

Each State Partition History has indices which always match those of the Cumulative Timesteps History, so they are always synchronised with each other.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-history.svg" width=600/></center>

## Example: Energy usage in a smart building

```{=html}
<div id="sim-history-demo" style="margin:1.5em 0;padding:1em;background:#ffffff;">
  <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;margin-bottom:0.9em;">
    <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Overall time series (Temperature)</div>
    <svg id="sim-history-overall" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Overall time series"></svg>
    <div style="font-size:1rem;color:#2c3e50;padding:0 0.75em;margin-bottom:0.35em;">Highlighted window corresponds to the History panels below.</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:0.9em;">
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Cumulative Timesteps History</div>
      <svg id="sim-history-timeline" width="100%" height="140" viewBox="0 0 320 140" role="img" aria-label="Cumulative timesteps history"></svg>
      <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">The most recent Time is at the top.</div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">State Partition Histories</div>
      <svg id="sim-history-partitions" width="100%" height="140" viewBox="0 0 320 140" role="img" aria-label="State partition histories"></svg>
      <div id="sim-history-state" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;margin-bottom:0.35em;"></div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.8em;">
    <button id="sim-history-step" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Advance 1 Timestep
    </button>
    <button id="sim-history-reset" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      New Simulation Run
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
        <div><strong>Latest Simulation State:</strong> Occupancy ${latest.occupancy}, Temperature ${latest.temperature.toFixed(1)}°C.</div>
        <div>Both Histories are indexed by the same Times.</div>
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

## Computing the next timesteps

So new States of the simulation may happen at different Times. But what determines when these Times are along the Simulation Timeline?

When simulating systems in the real world, it can be desireable in some situations to be able to structure the Times along the Timeline at regular intervals.

In other situations it can be desirable to have an unstructured or randomly-drawn set of Times along the Timeline.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/timeline.svg" /></center>

In order to allow this flexibility in choice between situations, let's specify an 'Advance Time' calculation which takes in the current Cumulative Timesteps History and outputs the Next Timestep following the latest Time found in the History (at index 0).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/advance-time.svg" /></center>

## State partition iteration

For an overall simulation data view, we can create a 'State Partition Histories' structure. This is a collection of each State Partition History that exists within the simulation.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/state-partition-histories.svg" width=600/></center>

How do we determine the 'Next Values' of each State Partition in Time?

This is where we should maintain full flexibility in choice of calculation so that our simulation is able to represent many different real-world systems.

Each of these calculations for a given Partition specifies how the State Partition Histories and Cumulative Timesteps History data are used to determine the Next Values of the State Partition.

In order to support even more flexibility in configuration, the calculation should also take in a set of Parameters which are specific to that Partition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-iteration.svg" /></center>

## State partition and time updates

Having calculated the Next Values of each State Partition and the Next Timestep, we should perform operations over the Cumulative Timesteps History and each State Partition History to Update their structures with this new data.

This is an important procedure to perform all at once to ensure that the all of the State Partitions in the simulation are synchronised against its virtual clock.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/update-time-history.svg" /></center>

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/update-state-partition-history.svg" /></center>

## Composing and coordinating partitions

So far we have considered Partition Iterations as occurring separately within the simulation. But it is important for these separate Partitions to be able to pass information to each other. 

To understand why this is important, think of our sports team example earlier and how each player might change their behaviour depending on the positions of other players on the field. They need to know about each other.

So how do we compose Partitions together so that information may be passed between them? 

In some sense, this happens already. Each Partition may read information from the State Partition Histories in the Iteration to its Next Values.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-timeline-composition.svg" /></center>

This composition allows us to correlate the behaviour of Partitions in Time.

We might also want to coordinate the Iterations of Partitions to occur in a particular order, where the first Iteration may then pass its calculated Next Values immediately into the second.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/partition-dependencies.svg" /></center>

For example, an Iteration might calculate the Mean statistic from some data and another might calculate the Variance. The Variance depends on the Mean so we need the Mean Next Values to be passed directly into the Variance to make sure these are always aligned in Time.

To enable coordination, all we need is for a 'Computationally Upstream' Iteration to be allowed to pass its Next Values into the Parameters of a 'Computationally Downstream' Iteration.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/composing-partitions.svg" /></center>

## Simulation runs

A 'Simulation Run' defines the evolution of a simulation State over some specified period in Time. 

Each Simulation Run has an Initial Time defined by an exact value, but the _end_ Time may not be known exactly until the simulation has evolved to meet some Termination Condition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/simulation-run.svg"/></center>

The Termination Condition logically determines when the Simulation Run should end according to a pre-defined calculation.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/termination-condition.svg"/></center>

## Embedded simulation runs

Enabling whole 'Inner' Simulation Runs to start and complete within each Timestep of an 'Outer' Simulation Run is a very useful, and somewhat fundamental, building block for simulations in practice. We shall call these 'Embedded Simulation Runs'.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-simulation-run.svg"/></center>

There are then several ways one can think of to pass information from the Outer simulation into the Inner simulation prior to running it on each Timestep.

Treating the Inner simulation as a Partition of the Outer simulation, one example is to simply pass Parameters from the Outer simulation into the Inner simulation, and nothing else.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/the_building_blocks_of_simulations/embedded-sim-iterate.svg" width=600/></center>

Another example is to pass both the Cumulative Timesteps History and State Partition Histories from the Outer simulation into the Inner simulation, in addition to the Parameters.

Consider how this might be used to create useful statistical operations over the history of the Outer simulation, e.g., like rolling window averages.

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
      Advance Outer Simulation
    </button>
    <button id="embedded-run-reset" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      New Outer Simulation Run
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
    })).textContent = "Embedded Simulation Run";

    if (stateBox) {
      stateBox.innerHTML = `
        <div><strong>Outer Simulation State:</strong> t=${sim.time}, Occupancy ${sim.occupancy}, Temperature ${sim.temperature.toFixed(1)}°C.</div>
        <div><strong>Embedded Simulation Run:</strong> forecast ${horizon} Timesteps ahead from the current State.</div>
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
