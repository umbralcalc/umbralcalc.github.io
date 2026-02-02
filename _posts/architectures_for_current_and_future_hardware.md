---
title: "Architectures for current and future hardware"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
order: 4
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/cpu-graph-edges.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/cpu-stepwise-architectures.svg"
---

# Architectures for current and future hardware
<div style="height:0.75em;"></div>

## Classical hardware

When we talk about 'classical' hardware here, we just mean standard CPUs.

On CPUs, simulation architectures may be constructed out of several ingredients. Loosely speaking, these are: Memory, Threads, Channels between Threads, Processes and Inter-Process Communication (IPC).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/cpu-graph-edges.svg"/></center>

All of these ingredients have their own tradeoffs in performance. But they are all useful in constructing the right simulation architectures to satisfy the right use cases.

In all of the previous posts so far, the main simulation architectures we have been considering are defined as Stepwise; simulation architectures which evaluate the Next State Values for the system at each point in Time, in turn.

Stepwise simulation architectures on CPUs are typically more performant when using Memory, Threads and Channels between Threads in the right combinations.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/cpu-stepwise-architectures.svg" width=600/></center>

In contrast, Processes, and IPC in particular, are typically more useful when we consider scaling computations in parallel across multiple non-interacting simulation Trajectories (which don't need much IPC). This is because IPC comes with more performance limitations.

Batch simulation architectures evaluate multiple successive sequences of Next State Values for the system over a wider interval in Time all as one computational block.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/stepwise-vs-batch.svg" width=600/></center>

Despite their appearance, Batch simulation architectures cannot fundamentally evaluate the Next State Values at different Timesteps in a truly parallel fashion. Simulations must still preserve the causal relationships between these Next State Values as they progress in Time.

To ensure this causality, some form of Iteration can be performed; like the Stepwise architecture implies by evaluating it recursively. 

However, it is sometimes sufficient to simply encode the causal/temporal dependencies between State Values along the Simulation Timeline as part of a Batch prediction; which is how some Machine Learning models are used to predict time series data.

## Example: Stepwise vs batch

```{=html}
<div id="stepwise-batch-demo" style="margin:0.5em 0;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Stepwise vs Batch Simulation Timeline</div>
  <svg id="stepwise-batch-svg" width="100%" height="170" viewBox="0 0 320 170" role="img" aria-label="Stepwise vs batch timeline"></svg>
  <div id="stepwise-batch-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-bottom:1em;">
  <label for="stepwise-batch-size" style="font-size:1rem;color:#2c3e50;">Batch size</label>
  <input id="stepwise-batch-size" type="range" min="1" max="6" value="3" step="1" style="accent-color:#3c78d8;width:160px;">
  <div id="stepwise-batch-value" style="font-size:1rem;color:#2c3e50;"></div>
</div>
<script>
(() => {
  const svg = document.getElementById("stepwise-batch-svg");
  const slider = document.getElementById("stepwise-batch-size");
  const value = document.getElementById("stepwise-batch-value");
  const text = document.getElementById("stepwise-batch-text");
  if (!svg || !slider || !value || !text) return;

  const width = 320;
  const height = 170;
  const pad = 18;
  const steps = 12;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const render = () => {
    const batchSize = parseInt(slider.value, 10);
    value.textContent = `${batchSize} Timesteps`;
    svg.innerHTML = "";

    const laneY = {
      stepwise: pad + 28,
      batch: pad + 96,
    };
    const barW = (width - 2 * pad) / steps;

    svg.appendChild(createSvgEl("text", {
      x: pad,
      y: pad + 12,
      fill: "#2c3e50",
      "font-size": "10",
    })).textContent = "stepwise";

    svg.appendChild(createSvgEl("text", {
      x: pad,
      y: laneY.batch - 14,
      fill: "#2c3e50",
      "font-size": "10",
    })).textContent = "batch";

    for (let i = 0; i < steps; i += 1) {
      const x = pad + i * barW;
      svg.appendChild(createSvgEl("rect", {
        x,
        y: laneY.stepwise,
        width: barW - 2,
        height: 18,
        fill: "#3c78d8",
      }));
    }

    for (let i = 0; i < steps; i += batchSize) {
      const x = pad + i * barW;
      const span = Math.min(batchSize, steps - i);
      svg.appendChild(createSvgEl("rect", {
        x,
        y: laneY.batch,
        width: span * barW - 2,
        height: 18,
        fill: "#b0447a",
      }));
    }

    svg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: height - pad,
      x2: width - pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    text.innerHTML = `
      <div>Batch evaluation groups multiple Timesteps, but the causal order still flows left-to-right.</div>
    `;
  };

  slider.addEventListener("input", render);
  render();
})();
</script>
```

## Specialised classical hardware

From the perspective of standard CPUs, Batch simulation architectures are often designed to evaluate segments of the Simulation Timeline using specialised classical hardware.

When we talk about 'specialised classical' hardware here, we mean [GPUs](https://en.wikipedia.org/wiki/Graphics_processing_unit), [TPUs](https://en.wikipedia.org/wiki/Tensor_Processing_Unit), [IPUs](https://www.graphcore.ai/products/ipu) and other specialised processors based on classical computing principles (as opposed to quantum processors).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/specialised-classical-batch.svg"/></center>

This architecture can be used to reduce the overall processing time taken to complete a Simulation Run relative to a Stepwise equivalent, but there are tradeoffs which mean this isn't always efficient.

GPUs, TPUs, IPUs, etc. all have their limitations. For example, GPUs and TPUs are highly optimised for dense arithmetic operations but struggle with branching control flow. IPUs offer more flexibility for irregular compute patterns and sparse operations, though they still prioritise throughput over the complex sequential logic that CPUs handle well.

So there are basically certain types of simulation algorithm that can be written that GPUs, TPUs, IPUs, etc. are not well-suited to reducing the overall processing time for.

In addition, this specialised hardware typically requires data transfer to/from CPU Memory (at the very least for initialisation and final results), which also takes processing time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/processing-time-per-timestep.svg"/></center>

So, when deciding on the number of Timesteps a Batch simulation architecture should use for the best performance, software engineers must take into account:

- the available Memory of their specialised hardware
- the Memory requirements for their simulation State Partition Histories
- the overall number of Timesteps they need to perform
- the implications this has on the number of I/O operations needed to interact with CPU Memory
- and the implications _this_ has on reducing the overall processing time, given the specialised hardware.

## Example: Batch size tradeoffs

```{=html}
<div id="transfer-bottleneck-demo" style="margin:0.5em 0;padding:1em;background:#ffffff;border:1px solid #2c3e50;border-radius:6px;">
  <svg id="transfer-bottleneck-svg" width="100%" height="180" viewBox="0 0 320 180" role="img" aria-label="Transfer vs compute trade-off"></svg>
  <div id="transfer-bottleneck-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
</div>
<div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.3em">
  <label for="transfer-bottleneck-size" style="font-size:1rem;color:#2c3e50;">Batch size</label>
  <input id="transfer-bottleneck-size" type="range" min="1" max="12" value="4" step="1" style="accent-color:#3c78d8;width:160px;">
  <div id="transfer-bottleneck-value" style="font-size:1rem;color:#2c3e50;"></div>
</div>
<script>
(() => {
  const svg = document.getElementById("transfer-bottleneck-svg");
  const slider = document.getElementById("transfer-bottleneck-size");
  const value = document.getElementById("transfer-bottleneck-value");
  const text = document.getElementById("transfer-bottleneck-text");
  if (!svg || !slider || !value || !text) return;

  const width = 320;
  const height = 180;
  const pad = 18;
  const maxBatch = 12;
  const memoryLimit = 8;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    return el;
  };

  const computeCost = (batchSize) => 4 + 0.7 * batchSize;
  const transferCost = (batchSize) => 14 + 18 / batchSize;

  const maxTotal = () => {
    let max = 0;
    for (let b = 1; b <= maxBatch; b += 1) {
      const total = computeCost(b) + transferCost(b);
      if (total > max) max = total;
    }
    return max;
  };

  const render = () => {
    const batchSize = parseInt(slider.value, 10);
    value.textContent = `${batchSize} Timesteps (available Memory: ${memoryLimit})`;
    svg.innerHTML = "";

    const total = computeCost(batchSize) + transferCost(batchSize);
    const maxVal = maxTotal();
    const innerHeight = height - 2 * pad;
    const scale = innerHeight / maxVal;

    svg.appendChild(createSvgEl("line", {
      x1: pad,
      y1: height - pad,
      x2: width - pad,
      y2: height - pad,
      stroke: "#2c3e50",
      "stroke-width": "1",
    }));

    const barX = width / 2 - 24;
    const barW = 48;
    const transferH = transferCost(batchSize) * scale;
    const computeH = computeCost(batchSize) * scale;
    const baseY = height - pad;

    const barColor = batchSize > memoryLimit ? "#111111" : "#3c78d8";
    const transferColor = batchSize > memoryLimit ? "rgba(176,68,122,0.35)" : "#b0447a";

    svg.appendChild(createSvgEl("rect", {
      x: barX,
      y: baseY - transferH,
      width: barW,
      height: transferH,
      fill: transferColor,
    }));
    svg.appendChild(createSvgEl("rect", {
      x: barX,
      y: baseY - transferH - computeH,
      width: barW,
      height: computeH,
      fill: barColor,
    }));

    if (memoryLimit > 0) {
      const capY = baseY - (computeCost(memoryLimit) + transferCost(memoryLimit)) * scale;
      svg.appendChild(createSvgEl("line", {
        x1: barX - 12,
        y1: capY,
        x2: barX + barW + 12,
        y2: capY,
        stroke: "#2c3e50",
        "stroke-width": "1",
        "stroke-dasharray": "4 3",
      }));
      svg.appendChild(createSvgEl("text", {
        x: barX + barW + 14,
        y: capY + 4,
        fill: "#2c3e50",
        "font-size": "10",
      })).textContent = "available Memory";
    }

    svg.appendChild(createSvgEl("text", {
      x: barX + barW + 8,
      y: baseY - transferH + 12,
      fill: "#2c3e50",
      "font-size": "10",
    })).textContent = "I/O processing time";
    svg.appendChild(createSvgEl("text", {
      x: barX + barW + 8,
      y: baseY - transferH - computeH + 12,
      fill: "#2c3e50",
      "font-size": "10",
    })).textContent = "Batch processing time";

    text.innerHTML = `
      <div>I/O cost per Timestep falls with larger Batches, while Batch processing time grows.</div>
      <div>Available Memory limits how large the Batch can be.</div>
      ${batchSize > memoryLimit ? "<div><strong>Warning:</strong> Batch size exceeds available Memory.</div>" : ""}
    `;
  };

  slider.addEventListener("input", render);
  render();
})();
</script>
```

## Quantum hardware

Note that the concepts in this section are the most likely to change with future advancements in Quantum Computing.

Quantum hardware seems to naturally fit the Batch simulation architecture in the same way that specialised classical hardware does.

In order to utilise this hardware within a given Batch evaluation, one would need to:

- prepare the initial state of [Qubits](https://en.wikipedia.org/wiki/Qubit)
- encode the State Partition Histories from CPU Memory into these Qubits
- run quantum gates which encode the logic for multiple Timesteps of the simulation
- entangle the Next State Values at each Timestep with [Ancilla Qubits](https://en.wikipedia.org/wiki/Ancilla_bit) or rely on the Qubits for State Partition Histories themselves
- and measure these Next State Values in order to write the data to CPU Memory.

Note also that the [No-Cloning Theorem](https://en.wikipedia.org/wiki/No-cloning_theorem) means we cannot simply copy the Qubits which have run the quantum gates; the circuit must run separately for each simulation Trajectory.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/architectures_for_current_and_future_hardware/quantum-batch.svg"/></center>

Therefore, you only get a [Quantum Advantage](https://en.wikipedia.org/wiki/Quantum_supremacy) if you can store more than one Timestep worth of simulation Next State Values in Qubit Memory. 

Otherwise, if you only effectively have one instantaneous Timestep of Qubit Memory to use, the processing time will likely be dominated by I/O writing to and from the Qubits during the simulation. This is also known as the [Quantum I/O Bottleneck](https://ianreppel.org/io-bottleneck-in-quantum-computing/).
