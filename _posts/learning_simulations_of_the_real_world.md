---
title: "Learning simulations of the real world"
tag: "How can I simulate the real world?"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals of simulation technology and how it can be useful to the world. No maths; just diagrams and straightforward descriptions all the way through."
order: 4
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/data-streaming.svg"
---

# Learning simulations of the real world
<div style="height:0.75em;"></div>

## What is our objective?

Unlike machine learning models, which typically come with standard training algorithms (like [backpropagation](https://en.wikipedia.org/wiki/Backpropagation) for neural networks), simulations often need us to explicitly choose and design procedures for learning their parameters from real-world data or optimising their outputs.

In order to do this, we must first have some objective which either characterises how close simulation trajectories are to replicating the data we have or define the quantity we want to optimise.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"/></center>

There are a number of techniques we can use to specify what the objective should be, depending on the purpose.

## Learning parameters from data

If we want to learn the parameters which correspond to simulation trajectories fitting real-world data trends more closely, it is natural to use an objective based on the probabilities of state partition histories that we computed in the previous post.

We start by streaming time-series data into our simulation by specifying it as a state partition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/data-streaming.svg" width="650"/></center>

We can then use a method to estimate the probabilities of state values within the data, e.g., the probabilistic sample weighting we discussed in the previous post.

So we have a way to calculate these 'data probabilities' for any possible state values the data can take in time.

By then evaluating these data probabilities at the points which coincide with simulation trajectories, we have an objective which quantifies how close the simulation is to the data.

When talking about different values for this objective, we often use the terminology 'quality of fit' or 'fit to the data' to describe how close the simulation is to replicating the data, and hence how good the value of the objective is.

## Example: Online simulation parameter estimation

The data probabilities of simulation trajectories can also be interpreted as probabilities of simulation parameters; often accompanied with some simulation noise to account for differences between trajectories even with the same parameters.

We can create an algorithm which uses this sequence of probabilities to estimate the probabilities of simulation parameters in a very similar way to probabilistic sample weighting (see the last post for details on the latter).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/online-posterior-estimation.svg"/></center>

We might call this algorithm 'online simulation parameter estimation'; where 'online' here means that the simulation is being adaptively learned to the data iteratively in time, as opposed to a whole batch all at once.

````{=html}
<div id="online-estimation-demo" style="margin:1.3em 0 0.5em;padding:1em;background:#ffffff;">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.9em;">
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Observed data vs estimated trajectory</div>
      <svg id="online-est-traj-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Observed data and estimated trajectory"></svg>
      <div id="online-est-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Parameter posterior estimate</div>
      <svg id="online-est-param-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Parameter posterior estimate"></svg>
      <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Each bar estimates how plausible a particular θ value is given the data.</div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.5em;margin-bottom:1em;">
    <button id="online-est-step" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Advance 5 timesteps
    </button>
    <button id="online-est-reset" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Reset simulation
    </button>
  </div>
</div>
<script>
(() => {
  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    return el;
  };
  const randn = () => {
    const u = Math.random(), v = Math.random();
    return Math.sqrt(-2 * Math.log(u || 1e-10)) * Math.cos(2 * Math.PI * v);
  };

  const nParticles = 40;
  const noiseStd = 0.4;
  const driftScale = 0.15;

  let state;
  const init = () => {
    const trueTheta = (Math.random() - 0.5) * 2.4;
    const particles = [];
    for (let i = 0; i < nParticles; i++) {
      particles.push({ theta: randn() * 1.2, weight: 1 / nParticles, x: 0 });
    }
    state = { trueTheta, trueX: 0, data: [0], particles, time: 0, weightedMean: [0] };
  };

  const advance = (steps) => {
    for (let s = 0; s < steps; s++) {
      state.time++;
      state.trueX += state.trueTheta * driftScale + randn() * noiseStd;
      state.data.push(state.trueX);

      let totalWeight = 0;
      state.particles.forEach(p => {
        p.x += p.theta * driftScale + randn() * noiseStd;
        const diff = state.trueX - p.x;
        p.weight *= Math.exp(-0.5 * (diff * diff) / (noiseStd * noiseStd));
        totalWeight += p.weight;
      });
      if (totalWeight > 0) state.particles.forEach(p => p.weight /= totalWeight);

      const ess = 1 / state.particles.reduce((s, p) => s + p.weight * p.weight, 0);
      if (ess < nParticles / 3) {
        const cumW = []; let cs = 0;
        state.particles.forEach(p => { cs += p.weight; cumW.push(cs); });
        const np = []; const u0 = Math.random() / nParticles; let j = 0;
        for (let i = 0; i < nParticles; i++) {
          const u = u0 + i / nParticles;
          while (j < nParticles - 1 && cumW[j] < u) j++;
          np.push({ theta: state.particles[j].theta + randn() * 0.05, weight: 1 / nParticles, x: state.particles[j].x });
        }
        state.particles = np;
      }
      let wm = 0;
      state.particles.forEach(p => wm += p.weight * p.x);
      state.weightedMean.push(wm);
    }
  };

  const render = () => {
    const trajSvg = document.getElementById("online-est-traj-svg");
    const paramSvg = document.getElementById("online-est-param-svg");
    trajSvg.innerHTML = ""; paramSvg.innerHTML = "";
    const w = 320, h = 160, pad = 18;

    if (state.data.length > 1) {
      const allVals = [...state.data, ...state.weightedMean];
      const minV = Math.min(...allVals) - 0.5, maxV = Math.max(...allVals) + 0.5;
      const n = state.data.length;
      const toX = i => pad + (i / Math.max(n - 1, 1)) * (w - 2 * pad);
      const toY = v => h - pad - ((v - minV) / (maxV - minV || 1)) * (h - 2 * pad);

      trajSvg.appendChild(createSvgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#2c3e50", "stroke-width": "1" }));
      trajSvg.appendChild(createSvgEl("path", {
        d: state.data.map((v, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(v)}`).join(" "),
        fill: "none", stroke: "#2c3e50", "stroke-width": "2"
      }));
      trajSvg.appendChild(createSvgEl("path", {
        d: state.weightedMean.map((v, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(v)}`).join(" "),
        fill: "none", stroke: "#3c78d8", "stroke-width": "2", "stroke-dasharray": "5 3"
      }));
      const leg = createSvgEl("text", { x: pad + 4, y: pad + 6, fill: "#2c3e50", "font-size": "10", "font-family": "system-ui,sans-serif" });
      leg.textContent = "\u2014 Data"; trajSvg.appendChild(leg);
      const leg2 = createSvgEl("text", { x: pad + 52, y: pad + 6, fill: "#3c78d8", "font-size": "10", "font-family": "system-ui,sans-serif" });
      leg2.textContent = "- - Estimated"; trajSvg.appendChild(leg2);
    } else {
      const t = createSvgEl("text", { x: w / 2, y: h / 2, fill: "#2c3e50", "font-size": "11", "text-anchor": "middle", "font-family": "system-ui,sans-serif" });
      t.textContent = "Press \u2018Advance\u2019 to stream data"; trajSvg.appendChild(t);
    }

    const nBins = 15, thetaMin = -2.8, thetaMax = 2.8;
    const binW = (thetaMax - thetaMin) / nBins;
    const bins = new Array(nBins).fill(0);
    state.particles.forEach(p => {
      const b = Math.floor((p.theta - thetaMin) / binW);
      if (b >= 0 && b < nBins) bins[b] += p.weight;
    });
    const maxBin = Math.max(...bins, 0.01);
    const barW = (w - 2 * pad) / nBins;

    paramSvg.appendChild(createSvgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#2c3e50", "stroke-width": "1" }));
    bins.forEach((b, i) => {
      const barH = (b / maxBin) * (h - 2 * pad - 12);
      if (barH > 0.5) {
        paramSvg.appendChild(createSvgEl("rect", {
          x: pad + i * barW + 1, y: h - pad - barH,
          width: Math.max(barW - 2, 1), height: barH,
          fill: "#3c78d8", opacity: "0.7", rx: "1"
        }));
      }
    });
    const trueX = pad + ((state.trueTheta - thetaMin) / (thetaMax - thetaMin)) * (w - 2 * pad);
    paramSvg.appendChild(createSvgEl("line", { x1: trueX, y1: pad, x2: trueX, y2: h - pad, stroke: "#b0447a", "stroke-width": "2", "stroke-dasharray": "4 3" }));
    const tl = createSvgEl("text", { x: trueX + 4, y: pad + 10, fill: "#b0447a", "font-size": "10", "font-family": "system-ui,sans-serif" });
    tl.textContent = "True \u03b8"; paramSvg.appendChild(tl);
    const al = createSvgEl("text", { x: pad, y: h - pad + 12, fill: "#2c3e50", "font-size": "9", "font-family": "system-ui,sans-serif" });
    al.textContent = thetaMin.toFixed(1); paramSvg.appendChild(al);
    const ar = createSvgEl("text", { x: w - pad - 14, y: h - pad + 12, fill: "#2c3e50", "font-size": "9", "font-family": "system-ui,sans-serif" });
    ar.textContent = thetaMax.toFixed(1); paramSvg.appendChild(ar);

    const wMean = state.particles.reduce((s, p) => s + p.weight * p.theta, 0);
    document.getElementById("online-est-text").textContent =
      "t = " + state.time + " \u00b7 True \u03b8 = " + state.trueTheta.toFixed(2) + " \u00b7 Estimated \u03b8 = " + wMean.toFixed(2);
  };

  init(); render();
  document.getElementById("online-est-step").addEventListener("click", () => { advance(5); render(); });
  document.getElementById("online-est-reset").addEventListener("click", () => { init(); render(); });
})();
</script>
````

## Simulation sloppiness isn't bad

So we have a simulation which is able to learn its parameters from real world data.

How sensitive is the simulation-data fit to changes in the parameters? In other words, how _sloppy_ is the simulation?

If a simulation is [sloppy](https://sethna.lassp.cornell.edu/Teaching/BasicTraining/SloppyBT24.html) it means that it has many additional parameters which can be varied that do not strongly affect the quality of fit to the dataset of interest. We typically call this kind of parameter 'unconstrained' by the data.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/sloppiness-vs-parsimony.svg" width="650"/></center>

Simulation sloppiness sounds bad; but [it has been shown](https://arxiv.org/abs/2505.08915) that machine learning models with more sloppiness have a tendency to generalise better to new datasets.

## Learning simulation structure from data

There is usually more than one simulation structure that can be a viable model for the real world system of interest, and these often have different numbers of parameters.

Choosing between different simulation structures should, in principle, be as easy as selecting the one with the best overall value for the objective. But it is actually more complicated than this because you can have complex or simple models which fit the data equally well.

Let's say we have two different simulation structures which we are comparing by fitting them to the same dataset. Let's also say that one of these simulations has lots of parameters and the other has much fewer.

We might interpret the concept of sloppiness to mean that the simulation which has more parameters is always the better choice. This would be wrong without a deeper analysis.

Remember that simulation sloppiness refers to parameters which _are not_ constrained by the data.

What we need to find out is how many parameters _are_ constrained (or learned) by the data in both simulations. In other words; how many parameters does each simulation have which the objective value is sensitive to changing?

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/simple-vs-complex-fit.svg"/></center>

The [general wisdom](https://en.wikipedia.org/wiki/Occam%27s_razor) is to prefer simulations and models with fewer _constrained_ parameters.

Why? Think about the parameter sensitivity of the quality of fit: if there are more parameters being constrained by the data, this means that the objective value is sensitive to more parameters. So there are more 'moving parts' to the simulation which have a greater chance of being misaligned with some new data we haven't seen yet.

We can think of simulations with fewer constrained parameters (but equal quality of fit) to be more likely to generalise across different datasets from a systems of the same, or similar, type in the real world. This also indicates more fundamental mechanisms are being learned from the data that are potentially transferrable to other systems.

## Example: Counting the parameters which are constrained

Let's imagine two different simulation structures being fit to the same dataset. The simple structure has 3 parameters, while the complex one has 7.

Let's also imagine that the complex structure always fits the observed data at least as well as the simple one; so the objective value on its own can never tell you which structure to choose.

Switching between the two structures, we can compare how many of their parameters the data actually constrains, and then use this as a way to choose between them.

````{=html}
<div id="constrained-params-demo" style="margin:1.3em 0 0.5em;padding:1em;background:#ffffff;">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.9em;">
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Fit to the observed data</div>
      <svg id="cp-fit-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Observed data with the fitted simulation trajectory"></svg>
      <div id="cp-fit-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">How far can each parameter move before the fit notices?</div>
      <svg id="cp-param-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Wiggle room of each simulation parameter"></svg>
      <div id="cp-param-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.5em;">
    <button id="cp-simple-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Simple structure (3 parameters)
    </button>
    <button id="cp-complex-btn" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Complex structure (7 parameters)
    </button>
    <button id="cp-trial-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Run a new trial
    </button>
  </div>
  <div id="cp-tally-text" style="font-size:1rem;color:#2c3e50;margin-top:0.6em;margin-bottom:1em;line-height:1.4;"></div>
</div>
<script>
(() => {
  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    return el;
  };
  const randn = () => {
    const u = Math.random(), v = Math.random();
    return Math.sqrt(-2 * Math.log(u || 1e-10)) * Math.cos(2 * Math.PI * v);
  };

  const nData = 16;
  const nUnseen = 60;
  const noiseStd = 0.25;
  const ridge = 1e-3;
  const wiggleScale = 2;
  const sloppyCut = 1.0;

  const cyc = (k, t) => Math.cos(k * Math.PI * t);
  const trueTrajectory = t => 1.0 + 0.6 * cyc(1, t) + 0.5 * cyc(2, t);

  const structures = {
    simple: {
      label: "simple structure",
      names: ["baseline", "trend", "seasonal"],
      effective: 3,
      basis: t => [1, cyc(1, t), cyc(2, t)]
    },
    complex: {
      label: "complex structure",
      names: ["baseline", "trend", "seasonal", "fast cycle", "faster cycle", "mechanism A", "mechanism B"],
      effective: 6,
      basis: t => [1, cyc(1, t), cyc(2, t), cyc(3, t), cyc(4, t), cyc(5, t), cyc(5, t)]
    }
  };

  const invert = (A) => {
    const n = A.length;
    const M = A.map((row, i) => [...row, ...Array.from({ length: n }, (_, j) => (i === j ? 1 : 0))]);
    for (let c = 0; c < n; c++) {
      let piv = c;
      for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[piv][c])) piv = r;
      [M[c], M[piv]] = [M[piv], M[c]];
      const d = M[c][c];
      for (let j = 0; j < 2 * n; j++) M[c][j] /= d;
      for (let r = 0; r < n; r++) {
        if (r === c) continue;
        const f = M[r][c];
        if (f) for (let j = 0; j < 2 * n; j++) M[r][j] -= f * M[c][j];
      }
    }
    return M.map(row => row.slice(n));
  };

  const predict = (structure, coef, t) =>
    structure.basis(t).reduce((s, v, i) => s + v * coef[i], 0);

  const rootMeanSqError = (structure, coef, dataset) =>
    Math.sqrt(dataset.ts.reduce((s, t, i) =>
      s + Math.pow(dataset.ys[i] - predict(structure, coef, t), 2), 0) / dataset.ts.length);

  const fitStructure = (structure, dataset) => {
    const X = dataset.ts.map(structure.basis);
    const p = X[0].length;
    const gram = Array.from({ length: p }, (_, i) =>
      Array.from({ length: p }, (_, j) =>
        X.reduce((s, x) => s + x[i] * x[j], 0) + (i === j ? ridge : 0)));
    const rhs = Array.from({ length: p }, (_, i) =>
      X.reduce((s, x, k) => s + x[i] * dataset.ys[k], 0));
    const gramInv = invert(gram);
    const coef = gramInv.map(row => row.reduce((s, v, j) => s + v * rhs[j], 0));

    const residualSq = dataset.ts.reduce((s, t, i) =>
      s + Math.pow(dataset.ys[i] - predict(structure, coef, t), 2), 0);
    const varHat = Math.max(residualSq / Math.max(dataset.ts.length - structure.effective, 1), 1e-8);
    const wiggle = gramInv.map((row, i) => wiggleScale * Math.sqrt(varHat * Math.max(row[i], 0)));

    return { coef, wiggle, fitError: Math.sqrt(residualSq / dataset.ts.length) };
  };

  const drawDataset = (n) => {
    const ts = Array.from({ length: n }, (_, i) => (i + 0.5) / n);
    return { ts, ys: ts.map(t => trueTrajectory(t) + randn() * noiseStd) };
  };

  let state;

  const runTrial = () => {
    const observed = drawDataset(nData);
    const unseen = drawDataset(nUnseen);
    const fits = {};
    const unseenError = {};
    Object.keys(structures).forEach(key => {
      fits[key] = fitStructure(structures[key], observed);
      unseenError[key] = rootMeanSqError(structures[key], fits[key].coef, unseen);
    });
    state.observed = observed;
    state.fits = fits;
    state.unseenError = unseenError;
    state.trials++;
    if (unseenError.simple < unseenError.complex) state.simpleWins++;
  };

  const init = () => {
    state = { shown: "simple", trials: 0, simpleWins: 0 };
    runTrial();
  };

  const renderFit = () => {
    const svg = document.getElementById("cp-fit-svg");
    svg.innerHTML = "";
    const w = 320, h = 160, padX = 18, padTop = 12, padBottom = 30;
    const structure = structures[state.shown];
    const coef = state.fits[state.shown].coef;

    const grid = Array.from({ length: 121 }, (_, i) => i / 120);
    const curve = grid.map(t => predict(structure, coef, t));
    const truth = grid.map(trueTrajectory);
    const allVals = [...state.observed.ys, ...curve, ...truth];
    const minV = Math.min(...allVals) - 0.2, maxV = Math.max(...allVals) + 0.2;
    const toX = t => padX + t * (w - 2 * padX);
    const toY = v => h - padBottom - ((v - minV) / (maxV - minV || 1)) * (h - padTop - padBottom);

    svg.appendChild(createSvgEl("line", {
      x1: padX, y1: h - padBottom, x2: w - padX, y2: h - padBottom,
      stroke: "#2c3e50", "stroke-width": "1"
    }));
    svg.appendChild(createSvgEl("path", {
      d: truth.map((v, i) => `${i === 0 ? "M" : "L"}${toX(grid[i])},${toY(v)}`).join(" "),
      fill: "none", stroke: "rgba(44,62,80,0.35)", "stroke-width": "2"
    }));
    svg.appendChild(createSvgEl("path", {
      d: curve.map((v, i) => `${i === 0 ? "M" : "L"}${toX(grid[i])},${toY(v)}`).join(" "),
      fill: "none", stroke: "#3c78d8", "stroke-width": "2"
    }));
    state.observed.ts.forEach((t, i) => {
      svg.appendChild(createSvgEl("circle", {
        cx: toX(t), cy: toY(state.observed.ys[i]), r: "2.4", fill: "#b0447a"
      }));
    });

    const legend = [
      { x: padX, colour: "#b0447a", text: "● Data" },
      { x: padX + 52, colour: "rgba(44,62,80,0.55)", text: "— True system" },
      { x: padX + 152, colour: "#3c78d8", text: "— Fitted" }
    ];
    legend.forEach(item => {
      const el = createSvgEl("text", {
        x: item.x, y: h - 8, fill: item.colour,
        "font-size": "10", "font-family": "system-ui,sans-serif"
      });
      el.textContent = item.text;
      svg.appendChild(el);
    });

    document.getElementById("cp-fit-text").textContent =
      "Fit error on this data · simple " + state.fits.simple.fitError.toFixed(3) +
      " · complex " + state.fits.complex.fitError.toFixed(3) +
      ". The complex structure always fits at least as well.";
  };

  const renderParams = () => {
    const svg = document.getElementById("cp-param-svg");
    svg.innerHTML = "";
    const w = 320, h = 160;
    const axisX0 = 78, axisX1 = 306, axisY = 126;
    const structure = structures[state.shown];
    const wiggle = state.fits[state.shown].wiggle;

    const logMin = Math.log(0.02), logMax = Math.log(20);
    const toX = value => {
      const clamped = Math.min(Math.max(value, 0.02), 20);
      return axisX0 + ((Math.log(clamped) - logMin) / (logMax - logMin)) * (axisX1 - axisX0);
    };

    const rowH = 15, top = 16, barH = 8;
    structure.names.forEach((name, i) => {
      const cy = top + i * rowH;
      const sloppy = wiggle[i] >= sloppyCut;
      const label = createSvgEl("text", {
        x: axisX0 - 6, y: cy + barH - 1, fill: "#2c3e50", "text-anchor": "end",
        "font-size": "9", "font-family": "system-ui,sans-serif"
      });
      label.textContent = name;
      svg.appendChild(label);
      svg.appendChild(createSvgEl("rect", {
        x: axisX0, y: cy, width: Math.max(toX(wiggle[i]) - axisX0, 1.5), height: barH,
        fill: sloppy ? "rgba(44,62,80,0.35)" : "#3c78d8", rx: "1"
      }));
    });

    svg.appendChild(createSvgEl("line", {
      x1: axisX0, y1: axisY, x2: axisX1, y2: axisY, stroke: "#2c3e50", "stroke-width": "1"
    }));
    const cutX = toX(sloppyCut);
    svg.appendChild(createSvgEl("line", {
      x1: cutX, y1: 10, x2: cutX, y2: axisY,
      stroke: "#b0447a", "stroke-width": "1.5", "stroke-dasharray": "4 3"
    }));

    const axisLabels = [
      { x: axisX0, anchor: "start", colour: "#3c78d8", text: "pinned down by the data" },
      { x: cutX + 4, anchor: "start", colour: "rgba(44,62,80,0.7)", text: "sloppy" }
    ];
    axisLabels.forEach(item => {
      const el = createSvgEl("text", {
        x: item.x, y: axisY + 13, fill: item.colour, "text-anchor": item.anchor,
        "font-size": "9", "font-family": "system-ui,sans-serif"
      });
      el.textContent = item.text;
      svg.appendChild(el);
    });
    const axisTitle = createSvgEl("text", {
      x: axisX0, y: h - 4, fill: "#2c3e50",
      "font-size": "9", "font-family": "system-ui,sans-serif"
    });
    axisTitle.textContent = "→ wiggle room, before the fit gets noticeably worse";
    svg.appendChild(axisTitle);

    const constrained = wiggle.filter(v => v < sloppyCut).length;
    document.getElementById("cp-param-text").textContent = state.shown === "simple"
      ? "The data pins down all " + constrained + " parameters, so there is nothing sloppy here."
      : "The data pins down " + constrained + " of the " + wiggle.length +
        " parameters. The last two are sloppy: they only ever affect the trajectory through their sum, so no amount of data can separate them.";
  };

  const renderTally = () => {
    document.getElementById("cp-tally-text").textContent =
      "On unseen data · simple " + state.unseenError.simple.toFixed(3) +
      " · complex " + state.unseenError.complex.toFixed(3) +
      ". The simple structure was closer in " + state.simpleWins + " of " + state.trials +
      (state.trials === 1 ? " trial." : " trials.");
  };

  const renderButtons = () => {
    const simpleBtn = document.getElementById("cp-simple-btn");
    const complexBtn = document.getElementById("cp-complex-btn");
    const selected = { border: "#3c78d8", background: "#3c78d8", color: "#ffffff" };
    const unselected = { border: "#2c3e50", background: "#ffffff", color: "#2c3e50" };
    const applyStyle = (btn, style) => {
      btn.style.borderColor = style.border;
      btn.style.background = style.background;
      btn.style.color = style.color;
    };
    applyStyle(simpleBtn, state.shown === "simple" ? selected : unselected);
    applyStyle(complexBtn, state.shown === "complex" ? selected : unselected);
  };

  const render = () => { renderFit(); renderParams(); renderTally(); renderButtons(); };

  init(); render();
  document.getElementById("cp-simple-btn").addEventListener("click", () => { state.shown = "simple"; render(); });
  document.getElementById("cp-complex-btn").addEventListener("click", () => { state.shown = "complex"; render(); });
  document.getElementById("cp-trial-btn").addEventListener("click", () => { runTrial(); render(); });
})();
</script>
````
