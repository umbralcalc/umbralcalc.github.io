---
title: "Building a simulation engine"
tag: "Simulating Real-World Systems as a Programmer"
order: 3
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-data-types.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/fundamental-loop-code.svg"
---

# Building a simulation engine
<div style="height:0.75em;"></div>

## Introducing the stochadex project

The building blocks of simulations that we have discussed can now be pieced together to form a complete simulation engine.

The [stochadex project](https://umbralcalc.github.io/stochadex) is an actual simulation engine written in Go which is based on these basic conceptual building blocks.

Armed with the fundamentals, we can now describe how this simulation engine was built in specific detail, supported by the appropriate system diagrams.

## Interfaces and data types

The fundamental data types in the stochadex simulation engine are Go types which can be configured as `Settings` (pure data) or `Implementations` (code which implements the provided interfaces).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-data-types.svg" /></center>

For example, we have the `Iteration` interface, which is based directly on the State Partition Iteration we discussed in the previous post.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/fundamental-loop-code.svg" /></center>

The `Iteration` interface can be used to implement any simulation in practice. To illustrate this point, we can show how the internal logic may be implemented to recreate some well-known stochastic processes.

For example, the [Wiener process](https://en.wikipedia.org/wiki/Wiener_process) has some very simple logic.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/wiener-process.svg" /></center>

```{=html}
<div id="wiener-demo" style="margin:0.5em 0;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Wiener process sample path</div>
  <svg id="wiener-svg" width="100%" height="170" viewBox="0 0 320 170" role="img" aria-label="Wiener process sample path"></svg>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.6em;margin-bottom:1em;">
  <button id="wiener-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    New sample path
  </button>
</div>
<script>
(() => {
  const svg = document.getElementById("wiener-svg");
  const btn = document.getElementById("wiener-btn");
  if (!svg || !btn) return;

  const width = 320;
  const height = 170;
  const pad = 18;
  const steps = 80;

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

  const render = () => {
    const values = [0];
    for (let i = 1; i <= steps; i += 1) {
      values.push(values[i - 1] + randn() * Math.sqrt(1 / steps));
    }
    const minVal = Math.min(...values);
    const maxVal = Math.max(...values);
    const range = maxVal - minVal || 1;

    svg.innerHTML = "";
    svg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: height - pad,
      x2: width - pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    const points = values.map((value, idx) => {
      const x = pad + (idx / steps) * (width - 2 * pad);
      const y = height - pad - ((value - minVal) / range) * (height - 2 * pad);
      return { x, y };
    });
    const path = points.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
    svg.appendChild(createSvgEl("path", {
      d: path,
      fill: "none",
      stroke: "#3c78d8",
      "stroke-width": "2",
    }));
  };

  btn.addEventListener("click", render);
  render();
})();
</script>
```

It is well-known (especially by those in finance) that [Itô's lemma](https://en.wikipedia.org/wiki/It%C3%B4%27s_lemma) can be used to adapt the model formulae for a Wiener process after a mathematical function (a.k.a. transformation) has been applied to it. 

We can demonstrate that the `Iteration` interface can support this kind of transformation as well, through some more complicated logic.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/ito-lemma.svg" /></center>

```{=html}
<div id="ito-demo" style="margin:0.5em 0;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Itô transform of a Wiener path</div>
  <svg id="ito-svg" width="100%" height="170" viewBox="0 0 320 170" role="img" aria-label="Ito transform example"></svg>
  <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Blue is the base path; pink is f(x)=x².</div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.6em;margin-bottom:1em;">
  <button id="ito-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    New transform
  </button>
</div>
<script>
(() => {
  const svg = document.getElementById("ito-svg");
  const btn = document.getElementById("ito-btn");
  if (!svg || !btn) return;

  const width = 320;
  const height = 170;
  const pad = 18;
  const steps = 80;

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

  const render = () => {
    const values = [0];
    for (let i = 1; i <= steps; i += 1) {
      values.push(values[i - 1] + randn() * Math.sqrt(1 / steps));
    }
    const transformed = values.map((value) => value * value);
    const minVal = Math.min(...values, ...transformed);
    const maxVal = Math.max(...values, ...transformed);
    const range = maxVal - minVal || 1;

    svg.innerHTML = "";
    svg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: height - pad,
      x2: width - pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    const mapPoints = (series) => series.map((value, idx) => {
      const x = pad + (idx / steps) * (width - 2 * pad);
      const y = height - pad - ((value - minVal) / range) * (height - 2 * pad);
      return { x, y };
    });

    const drawLine = (points, color, dash) => {
      const path = points.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
      svg.appendChild(createSvgEl("path", {
        d: path,
        fill: "none",
        stroke: color,
        "stroke-width": "2",
        "stroke-dasharray": dash || "none",
      }));
    };

    drawLine(mapPoints(values), "#3c78d8");
    drawLine(mapPoints(transformed), "#b0447a", "4 3");
  };

  btn.addEventListener("click", render);
  render();
})();
</script>
```

What about event-based processes?

The Time-Inhomogeneous [Poisson process](https://en.wikipedia.org/wiki/Poisson_point_process), is an example of an event-based process which counts the cumulative number of events in Time, while its event rate varies.

The `Iteration` interface can support this too.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/inhomogeneous-poisson.svg" /></center>

```{=html}
<div id="inhomogeneous-poisson-demo" style="margin:0.5em 0;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Inhomogeneous Poisson events</div>
  <svg id="inhomogeneous-poisson-svg" width="100%" height="170" viewBox="0 0 320 170" role="img" aria-label="Inhomogeneous Poisson process"></svg>
  <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Event ticks cluster where the rate curve is high.</div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.6em;margin-bottom:1em;">
  <button id="inhomogeneous-poisson-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    New event draw
  </button>
</div>
<script>
(() => {
  const svg = document.getElementById("inhomogeneous-poisson-svg");
  const btn = document.getElementById("inhomogeneous-poisson-btn");
  if (!svg || !btn) return;

  const width = 320;
  const height = 170;
  const pad = 18;
  const steps = 120;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const render = () => {
    svg.innerHTML = "";
    const rates = [];
    for (let i = 0; i <= steps; i += 1) {
      const t = i / steps;
      const rate = 0.6 + 0.8 * Math.sin(2 * Math.PI * t) + 0.4 * Math.sin(6 * Math.PI * t);
      rates.push(Math.max(0.1, rate));
    }
    const maxRate = Math.max(...rates);

    svg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: height - pad,
      x2: width - pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    const ratePoints = rates.map((rate, idx) => {
      const x = pad + (idx / steps) * (width - 2 * pad);
      const y = height - pad - (rate / maxRate) * (height - 2 * pad);
      return { x, y };
    });
    const path = ratePoints.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
    svg.appendChild(createSvgEl("path", {
      d: path,
      fill: "none",
      stroke: "#b0447a",
      "stroke-width": "2",
    }));

    const events = [];
    for (let i = 0; i <= steps; i += 1) {
      const t = i / steps;
      const rate = rates[i];
      const p = (rate / maxRate) * 0.18;
      if (Math.random() < p) {
        events.push(t);
      }
    }
    events.forEach((t) => {
      const x = pad + t * (width - 2 * pad);
      svg.appendChild(createSvgEl("line", {
        x1: x,
        y1: height - pad,
        x2: x,
        y2: height - pad - 14,
        stroke: "#3c78d8",
        "stroke-width": "2",
      }));
    });
  };

  btn.addEventListener("click", render);
  render();
})();
</script>
```

Let's give one more example.

The [Hawkes process](https://en.wikipedia.org/wiki/Hawkes_process) couples the history of events to the current event rate. One may therefore categorise this process as 'non-Markovian'.

This means that the Hawkes process needs a memory of the State Partition History in order to calculate its Next State Values. Based on everything we have already built and discussed, the `Iteration` interface obviously supports this quite easily.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/hawkes-process.svg" /></center>

```{=html}
<div id="hawkes-demo" style="margin:0.5em 0;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Hawkes process (self-exciting events)</div>
  <svg id="hawkes-svg" width="100%" height="170" viewBox="0 0 320 170" role="img" aria-label="Hawkes process"></svg>
  <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Events cluster because each event lifts the intensity.</div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.6em;margin-bottom:1em;">
  <button id="hawkes-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    New event draw
  </button>
</div>
<script>
(() => {
  const svg = document.getElementById("hawkes-svg");
  const btn = document.getElementById("hawkes-btn");
  if (!svg || !btn) return;

  const width = 320;
  const height = 170;
  const pad = 18;
  const steps = 120;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const render = () => {
    svg.innerHTML = "";
    const baseRate = 0.2;
    const alpha = 0.8;
    const beta = 6;
    const events = [];
    const intensities = [];

    for (let i = 0; i <= steps; i += 1) {
      const t = i / steps;
      let intensity = baseRate;
      events.forEach((time) => {
        intensity += alpha * Math.exp(-beta * (t - time));
      });
      intensities.push(intensity);
      const p = intensity * 0.12;
      if (Math.random() < p) {
        events.push(t);
      }
    }

    const maxIntensity = Math.max(...intensities);
    svg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: height - pad,
      x2: width - pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    const intensityPoints = intensities.map((value, idx) => {
      const x = pad + (idx / steps) * (width - 2 * pad);
      const y = height - pad - (value / maxIntensity) * (height - 2 * pad);
      return { x, y };
    });
    const path = intensityPoints.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
    svg.appendChild(createSvgEl("path", {
      d: path,
      fill: "none",
      stroke: "#b0447a",
      "stroke-width": "2",
    }));

    events.forEach((t) => {
      const x = pad + t * (width - 2 * pad);
      svg.appendChild(createSvgEl("line", {
        x1: x,
        y1: height - pad,
        x2: x,
        y2: height - pad - 14,
        stroke: "#3c78d8",
        "stroke-width": "2",
      }));
    });
  };

  btn.addEventListener("click", render);
  render();
})();
</script>
```

## Serial dependency graphs and modularity

Multiple `Iteration`s can run within the stochadex for each step in Time. In order to construct serial dependency graphs between them, we can utilise upstream-downstream `Iteration` relationships.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-parallel-serial.svg" /></center>

Structuring groups of `Iteration`s in this way can increase modularity. For example, the Time-Inhomogeneous Poisson process can be implemented serially.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/inhomo-poisson-parallel-serial.svg" /></center>

## Simulation loop and embedded simulation runs

The Simulation Run loop coordinates the serial relationships between `Iteration`s while maximising concurrency in execution of each `Iteration` per step in Time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/stochadex-loop.svg" /></center>

Given that this loop always runs for any stochadex simulation, it is sufficient to describe any simulation uniquely through the dependency diagram between its `Iteration`s.

Having designed the Simulation Run loop, are now finally able to implement Embedded Simulation Runs. 

As a reminder; Embedded Simulation Runs are `Iteration`s which perform entire Simulation Runs from start to end for every Timestep. Their presence can make the diagrams a little more complex, but even more flexible.

The `Iteration` interface can support these as well.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/building_a_simulation_engine/embedded-simulations.svg" /></center>
