---
title: "Learning simulations of the real world"
tag: "Simulating Real-World Systems as a Programmer"
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

## Simulation sloppiness

So we have a simulation which is able to learn its parameters from real world data.

How sensitive is the simulation-data fit to changes in the parameters? In other words, how _sloppy_ is the simulation?

If a simulation is [sloppy](https://sethna.lassp.cornell.edu/Teaching/BasicTraining/SloppyBT24.html) it means that it has many additional parameters which can be varied that do not strongly affect the quality of fit to the dataset of interest. We typically call this kind of parameter 'unconstrained' by the data.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/sloppiness-vs-parsimony.svg" width="650"/></center>

Simulation sloppiness sounds bad; but [it has been shown](https://arxiv.org/abs/2505.08915) that machine learning models with more sloppiness have a tendency to generalise better to new datasets.

## Learning simulation structure from data

Simulations with lots of parameters can have their downsides. 

Let's say we have two different simulation structures which we are comparing by fitting them to the same dataset. Let's also say that one of these simulations has lots of parameters and the other has much fewer.

We might interpret the concept of sloppiness to mean that the simulation which has more parameters is always the better choice. This would be wrong without a deeper analysis.

What we need to find out is how many parameters are being actively used to fit the data in both simulations. In other words; how many parameters does each simulation have which the quality fit is sensitive to changing?

In addition to answering this question, it's clearly important to have a way of discovering which simulation structure is better.

...

What I basically want to say is:
- Choosing between models should, in principle, be as easy as selecting the one with the best overall value for the objective
- It's more complicated than this because you can have complex or simple models which fit the data equally well
- Deciding between these two depends on the context of the problem, but the [general wisdom](https://en.wikipedia.org/wiki/Occam%27s_razor) is to prefer simulations and models with fewer constrained parameters
- Why is this? This sounds counterintuitive when you remember that sloppy simulations with more unconstrained parameters might generalise better to other problems
- Think about the parameter sensitivity of the quality of fit; if there are more parameters being constrained by the data, then the fit quality is sensitive to more parameters, and so there are more 'moving parts' to the simulation which could be misaligned with the next set of data we try to fit it to
- In this sense, we can think of simulations with fewer constrained parameters (but equal quality of fit to any alternative) to be more likely to generalise across different datasets within a domain - this is a valuable property to have, and indicates more fundamental mechanisms are being learned by the simulation