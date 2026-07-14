---
title: "Learning simulations of the real world"
tag: "Simulating Real-World Systems as a Programmer"
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals of simulation technology and how it can be useful to the world. No maths; just diagrams and straightforward descriptions all the way through."
order: 4
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/world-model-and-data.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"
---

# Learning simulations of the real world
<div style="height:0.75em;"></div>

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/world-model-and-data.svg" width="400" /></center>

## How do we learn a simulation?

Unlike machine learning models, which typically come with standard training algorithms (like [backpropagation](https://en.wikipedia.org/wiki/Backpropagation) for neural networks), simulations often need us to explicitly choose and design procedures for learning their parameters from real-world data or optimising their outputs.

In order to do this, we must first have some objective which either characterises how close simulation trajectories are to replicating the data we have or define the quantity we want to optimise.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/objectives.svg"/></center>

There are a number of techniques we can use to specify what the objective should be, depending on the purpose.

## Learning simulations from data

If we want to learn the parameters which correspond to simulation trajectories fitting real-world data trends more closely, it is natural to use an objective based on the probabilities of state partition histories that we computed in the previous post.

We start by streaming time-series data into our simulation by specifying it as a state partition.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/data-streaming.svg"/></center>

We can then use a method to estimate the probabilities of state values within the data, e.g., the probabilistic sample weighting we discussed in the previous post.

So we have a way to calculate these 'data probabilities' for any possible state values the data can take in time.

By then evaluating these data probabilities at the points which coincide with simulation trajectories, we have an objective which quantifies how close the simulation is to the data.

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

## Learning optimal simulations

If we want to learn parameters which correspond to optimal simulation trajectories, we first need to specify what 'optimal' means.

We do this by defining an objective whose maximum/minimum possible value will be achieved when our goal is met.

For instance, we may define some logic in a state partition iteration of the simulation which replicates taking 'actions' in the real world. This logic can depend on the simulation parameters so that the latter encodes the behaviour quantitatively.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/action-taking.svg"/></center>

Given this setup, a very common goal of interest is then in finding the best actions to take; which is analogous to optimising the parameters of the action-taking state partition iteration. We will refer to these parameters as 'policy parameters'.

But what should be use as an objective?

The 'discounted future reward' is a quantity we can specify that a simulation trajectory will have accumulated into the future, accounting for increasing distance into the future by 'discounting' it gradually with a weighting.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/discounted-future-reward.svg"/></center>

We are using this concept of discounted future reward in the same way that it is used in [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning).

The idea is that, as you go further into the future, the importance of the reward you have accumulated by then is increasingly irrelevant to actions you might take at the present moment.

## Example: Optimising with evolutionary strategies

The [evolutionary strategies](https://en.wikipedia.org/wiki/Evolution_strategy) algorithm can be applied to search future simulation trajectories to find the best set of policy parameters needed to achieve some discounted future reward.

This algorithm relies on sorting the sampled simulation trajectories according to their discounted future rewards and then using the top fraction of these to update the best known policy parameters (and the variance around them) after each timestep.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/optimising-evolutionary-strategies.svg"/></center>

````{=html}
<div id="evolutionary-strategies-demo" style="margin:1.3em 0 0.5em;padding:1em;background:#ffffff;">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.9em;">
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Sampled simulation trajectories</div>
      <svg id="es-traj-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Sampled simulation trajectories"></svg>
      <div style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Optimises best fraction of policy parameters (blue lines) towards the target. Grey lines are the others.</div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Best discounted future reward</div>
      <svg id="es-reward-svg" width="100%" height="160" viewBox="0 0 320 160" role="img" aria-label="Best discounted future reward over generations"></svg>
      <div id="es-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;line-height:1.4;padding:0 0.75em;"></div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.5em;margin-bottom:1em;">
    <button id="es-gen-btn" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Run 1 generation
    </button>
    <button id="es-reset-btn" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Reset optimisation
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

  const popSize = 20;
  const eliteCount = 5;
  const horizon = 12;
  const target = 3.0;
  const gamma = 0.9;
  const noise = 0.15;

  let state;
  const init = () => {
    state = {
      thetaMean: 0, thetaVar: 1.0,
      generation: 0, bestRewards: [],
      lastTrajectories: null, lastEliteIdx: null
    };
  };

  const runGeneration = () => {
    state.generation++;
    const trajectories = [];
    for (let p = 0; p < popSize; p++) {
      const theta = state.thetaMean + randn() * Math.sqrt(state.thetaVar);
      let x = 0; const path = [x];
      let reward = 0, discount = 1;
      for (let t = 0; t < horizon; t++) {
        x += theta * (target - x) * 0.3 + randn() * noise;
        path.push(x);
        reward += discount * (-Math.abs(x - target));
        discount *= gamma;
      }
      trajectories.push({ path, theta, reward });
    }
    const indices = trajectories.map((_, i) => i).sort((a, b) => trajectories[b].reward - trajectories[a].reward);
    const eliteIdx = new Set(indices.slice(0, eliteCount));
    const eliteThetas = indices.slice(0, eliteCount).map(i => trajectories[i].theta);
    const newMean = eliteThetas.reduce((s, t) => s + t, 0) / eliteCount;
    const newVar = Math.max(0.01, eliteThetas.reduce((s, t) => s + (t - newMean) ** 2, 0) / eliteCount);
    state.thetaMean = newMean;
    state.thetaVar = newVar;
    state.bestRewards.push(trajectories[indices[0]].reward);
    state.lastTrajectories = trajectories;
    state.lastEliteIdx = eliteIdx;
  };

  const render = () => {
    const trajSvg = document.getElementById("es-traj-svg");
    const rewardSvg = document.getElementById("es-reward-svg");
    trajSvg.innerHTML = ""; rewardSvg.innerHTML = "";
    const w = 320, h = 160, pad = 18;

    if (state.lastTrajectories) {
      let allVals = [target];
      state.lastTrajectories.forEach(t => t.path.forEach(v => allVals.push(v)));
      const minV = Math.min(...allVals) - 0.3, maxV = Math.max(...allVals) + 0.3;
      const toX = i => pad + (i / horizon) * (w - 2 * pad);
      const toY = v => h - pad - ((v - minV) / (maxV - minV || 1)) * (h - 2 * pad);

      trajSvg.appendChild(createSvgEl("line", {
        x1: pad, y1: toY(target), x2: w - pad, y2: toY(target),
        stroke: "#b0447a", "stroke-width": "1.5", "stroke-dasharray": "4 3"
      }));
      const tl = createSvgEl("text", { x: w - pad - 30, y: toY(target) - 5, fill: "#b0447a", "font-size": "9", "font-family": "system-ui,sans-serif" });
      tl.textContent = "Target"; trajSvg.appendChild(tl);
      trajSvg.appendChild(createSvgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#2c3e50", "stroke-width": "1" }));

      state.lastTrajectories.forEach((traj, idx) => {
        if (state.lastEliteIdx.has(idx)) return;
        trajSvg.appendChild(createSvgEl("path", {
          d: traj.path.map((v, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(v)}`).join(" "),
          fill: "none", stroke: "rgba(44,62,80,0.15)", "stroke-width": "1"
        }));
      });
      state.lastTrajectories.forEach((traj, idx) => {
        if (!state.lastEliteIdx.has(idx)) return;
        trajSvg.appendChild(createSvgEl("path", {
          d: traj.path.map((v, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(v)}`).join(" "),
          fill: "none", stroke: "rgba(60,120,216,0.55)", "stroke-width": "1.5"
        }));
      });
    } else {
      const t = createSvgEl("text", { x: w / 2, y: h / 2, fill: "#2c3e50", "font-size": "11", "text-anchor": "middle", "font-family": "system-ui,sans-serif" });
      t.textContent = "Press \u2018Run 1 generation\u2019 to start"; trajSvg.appendChild(t);
    }

    if (state.bestRewards.length > 0) {
      const n = state.bestRewards.length;
      const minR = Math.min(...state.bestRewards) - 0.3, maxR = Math.max(...state.bestRewards) + 0.3;
      const toX = i => pad + (i / Math.max(n - 1, 1)) * (w - 2 * pad);
      const toY = v => h - pad - ((v - minR) / (maxR - minR || 1)) * (h - 2 * pad);

      rewardSvg.appendChild(createSvgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#2c3e50", "stroke-width": "1" }));
      if (n > 1) {
        rewardSvg.appendChild(createSvgEl("path", {
          d: state.bestRewards.map((v, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(v)}`).join(" "),
          fill: "none", stroke: "#3c78d8", "stroke-width": "2"
        }));
      }
      state.bestRewards.forEach((v, i) => {
        rewardSvg.appendChild(createSvgEl("circle", { cx: toX(i), cy: toY(v), r: "3", fill: "#3c78d8" }));
      });
      const rl = createSvgEl("text", { x: pad + 2, y: pad + 8, fill: "#2c3e50", "font-size": "9", "font-family": "system-ui,sans-serif" });
      rl.textContent = "Best reward per generation"; rewardSvg.appendChild(rl);
    } else {
      const t = createSvgEl("text", { x: w / 2, y: h / 2, fill: "#2c3e50", "font-size": "11", "text-anchor": "middle", "font-family": "system-ui,sans-serif" });
      t.textContent = "Reward progress shown here"; rewardSvg.appendChild(t);
    }

    document.getElementById("es-text").textContent = state.generation > 0
      ? "Generation " + state.generation + " \u00b7 Policy \u03b8 mean = " + state.thetaMean.toFixed(2) + " \u00b7 Policy \u03b8 var = " + state.thetaVar.toFixed(3)
      : "";
  };

  init(); render();
  document.getElementById("es-gen-btn").addEventListener("click", () => { runGeneration(); render(); });
  document.getElementById("es-reset-btn").addEventListener("click", () => { init(); render(); });
})();
</script>
````
