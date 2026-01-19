---
title: "Why simulate real-world systems?"
tag: "Simulating Real-World Systems as a Programmer"
order: 1
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/why_simulate_real_world_systems/simulations-for-decisions.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/why_simulate_real_world_systems/simulations-decision-advantages.svg"
---

# Why simulate real-world systems?
<div style="height:0.75em;"></div>

## Who are these posts for?

These posts are aimed at programmers and non-technical readers wanting to learn the fundamentals of simulating real-world systems.

Together, we will explore the power of simulations and probabilistic thinking without the need for mathematical symbols.

Those eager to follow along with code should also check out the [stochadex project](https://umbralcalc.github.io/stochadex), which was designed with these fundamentals in mind. It is the main example of simulation software we will use throughout these posts.

## What can you do with these simulations?

One of the most compelling uses for simulations of real-world systems is in powering decision-making technologies.

If you want to answer questions like 'if I take this action, then what will happen in my system?', then it is often essential to build a simulation of your system and use this to simulate what might happen in the future.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/why_simulate_real_world_systems/simulations-for-decisions.svg" /></center>

## Advantages to using real-world simulations

With simulations of the real-world, in contrast to other predictive AI approaches, you can also interrogate the internal state of the system to help validate the assumptions used in making a decision.

This can be a real advantage for decision-making technologies, since human users usually need to justify their decisions through structured reasoning.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/why_simulate_real_world_systems/simulations-decision-advantages.svg" /></center>

## Example: Predictions only vs simulations

```{=html}
<div id="prediction-vs-model" style="margin:1.5em 0;padding:1em;background:#ffffff;">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.9em;">
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Prediction only</div>
      <svg id="ts-prediction-svg" width="100%" height="180" viewBox="0 0 320 180" role="img" aria-label="Prediction only chart"></svg>
      <div style="font-size:1rem;color:#2c3e50;margin-top:0;padding:0 0.75em;">There is a forecast line, but the internal logic is hidden. If the prediction is wrong, it's difficult to interrogate why.</div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Simulation/mechanistic model</div>
      <svg id="ts-model-svg" width="100%" height="180" viewBox="0 0 320 180" role="img" aria-label="Mechanistic model chart"></svg>
      <div id="ts-model-state" style="font-size:1rem;color:#2c3e50;margin-top:0;line-height:1.4;padding:0 0.75em;margin-bottom:0.35em;"></div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:space-between;margin-bottom:0.75em;"></div>
  <button id="ts-demo-generate" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
    Generate a new example
  </button>
</div>
<script>
(() => {
  const svgPrediction = document.getElementById("ts-prediction-svg");
  const svgModel = document.getElementById("ts-model-svg");
  const button = document.getElementById("ts-demo-generate");
  if (!svgPrediction || !svgModel || !button) return;

  const width = 320;
  const height = 180;
  const pad = 18;
  const totalPoints = 60;
  const pastPoints = 40;
  const forecastPoints = totalPoints - pastPoints;
  const period = 16;
  const trendSlope = 0.018;
  const trendIntercept = 0.15;
  const noiseLevel = 0.25;
  const stateBox = document.getElementById("ts-model-state");

  const randn = () => {
    let u = 0;
    let v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };

  const buildSeries = () => {
    const base = [];
    const observed = [];
    const phase = Math.random() * Math.PI * 2;
    for (let t = 0; t < totalPoints; t += 1) {
      const trend = trendIntercept + trendSlope * t;
      const seasonal = 0.55 * Math.sin((2 * Math.PI * t) / period + phase);
      const modelValue = trend + seasonal;
      base.push(modelValue);
      observed.push(modelValue + randn() * noiseLevel);
    }
    return { base, observed, phase };
  };

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const mapSeries = (values, minVal, maxVal, startIndex = 0) => {
    const range = maxVal - minVal || 1;
    return values.map((value, idx) => {
      const t = startIndex + idx;
      const x = pad + (t / (totalPoints - 1)) * (width - 2 * pad);
      const y = height - pad - ((value - minVal) / range) * (height - 2 * pad);
      return { x, y };
    });
  };

  const drawAxes = (svg) => {
    svg.appendChild(
      createSvgEl("line", {
        x1: pad,
        y1: height - pad,
        x2: width - pad,
        y2: height - pad,
        stroke: "#2c3e50",
        "stroke-width": "1",
      })
    );
    svg.appendChild(
      createSvgEl("line", {
        x1: pad,
        y1: pad,
        x2: pad,
        y2: height - pad,
        stroke: "#2c3e50",
        "stroke-width": "1",
      })
    );
  };

  const drawLine = (svg, points, options) => {
    const path = points.map((point, idx) => `${idx === 0 ? "M" : "L"}${point.x},${point.y}`).join(" ");
    svg.appendChild(
      createSvgEl("path", {
        d: path,
        fill: "none",
        stroke: options.color,
        "stroke-width": options.width || "2",
        "stroke-dasharray": options.dash || "none",
      })
    );
  };

  const drawPoints = (svg, points, options) => {
    points.forEach((point) => {
      svg.appendChild(
        createSvgEl("circle", {
          cx: point.x,
          cy: point.y,
          r: options.radius || 2.4,
          fill: options.color,
        })
      );
    });
  };

  const formatNumber = (value) => value.toFixed(2);

  const render = () => {
    const { base, observed, phase } = buildSeries();
    const trendValues = Array.from({ length: totalPoints }, (_, t) => trendIntercept + trendSlope * t);
    const modelMin = Math.min(...base, ...observed);
    const modelMax = Math.max(...base, ...observed);
    const basePoints = mapSeries(base, modelMin, modelMax);
    const observedPoints = mapSeries(observed, modelMin, modelMax);
    const trendPoints = mapSeries(trendValues, modelMin, modelMax);

    svgPrediction.innerHTML = "";
    svgModel.innerHTML = "";
    drawAxes(svgPrediction);
    drawAxes(svgModel);

    const futureStart = pastPoints - 1;
    const prediction = base
      .slice(pastPoints - 1)
      .map((value) => value + randn() * noiseLevel * 0.4);
    const predictionValues = observed.slice(0, pastPoints).concat(prediction);
    const predictionMin = Math.min(...predictionValues);
    const predictionMax = Math.max(...predictionValues);
    const pastObserved = mapSeries(
      observed.slice(0, pastPoints),
      predictionMin,
      predictionMax
    );
    const predictionPoints = mapSeries(
      prediction,
      predictionMin,
      predictionMax,
      futureStart
    );

    drawLine(svgPrediction, pastObserved, { color: "#2c3e50" });
    drawLine(svgPrediction, predictionPoints, { color: "#3c78d8", dash: "5 4" });
    const dividerX = pad + (futureStart / (totalPoints - 1)) * (width - 2 * pad);
    svgPrediction.appendChild(
      createSvgEl("line", {
        x1: dividerX,
        y1: pad,
        x2: dividerX,
        y2: height - pad,
        stroke: "#b0447a",
        "stroke-width": "1",
        "stroke-dasharray": "3 3",
      })
    );

    const modelObservedPast = observedPoints.slice(0, pastPoints);
    drawLine(svgModel, trendPoints, { color: "#3c78d8", dash: "4 3" });
    drawLine(svgModel, basePoints, { color: "#b0447a" });
    drawPoints(svgModel, modelObservedPast, { color: "#2c3e50" });
    svgModel.appendChild(
      createSvgEl("line", {
        x1: dividerX,
        y1: pad,
        x2: dividerX,
        y2: height - pad,
        stroke: "#3c78d8",
        "stroke-width": "1",
        "stroke-dasharray": "3 3",
      })
    );

    svgModel.appendChild(
      createSvgEl("text", {
        x: pad + 4,
        y: pad + 12,
        fill: "#2c3e50",
        "font-size": "10",
      })
    ).textContent = "observed points";
    svgModel.appendChild(
      createSvgEl("text", {
        x: pad + 4,
        y: pad + 26,
        fill: "#b0447a",
        "font-size": "10",
      })
    ).textContent = "model structure";

    if (stateBox) {
      stateBox.innerHTML = `
        <div"><strong>Simulation State:</strong> Trend slope ${formatNumber(trendSlope)}, Seasonal phase ${formatNumber(phase)}, Noise ${formatNumber(noiseLevel)}</div>
        <div"><strong>Assumptions:</strong> Linear trend + Periodic cycle + Random shocks.</div>
      `;
    }
  };

  button.addEventListener("click", render);
  render();
})();
</script>
```
