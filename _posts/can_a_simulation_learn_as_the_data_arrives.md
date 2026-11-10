---
title: "Can a simulation learn as the data arrives?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_simulations_of_the_real_world/online-posterior-estimation.svg"
cites:
- "[[how_does_a_simulation_learn_its_parameters_from_data]]"
- "[[can_one_trajectory_be_enough_to_estimate_statistics]]"
nocite: |
  @gordon1993, @doucet2011
---

# Can a simulation learn as the data arrives?
<div style="height:0.75em;"></div>

Yes, by updating its parameter estimates each time a new data point arrives rather than refitting to the whole batch. 

The data probabilities of simulation trajectories can be interpreted as probabilities of simulation parameters, often accompanied by some simulation noise to account for differences between trajectories even with the same parameters.

We can create an algorithm which uses this sequence of probabilities to estimate the probabilities of simulation parameters in a very similar way to probabilistic sample weighting.

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

## References and further reading

::: {#refs}
:::
