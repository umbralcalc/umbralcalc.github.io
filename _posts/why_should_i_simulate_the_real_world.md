---
title: Why should I simulate the real world?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/how-can-i-simulate-the-real-world-cover.svg
nocite: "@box1976, @cranmer2020, @epstein2008, @jumper2021, @lawkelton2014, @stochadex"
---
# Why should I simulate the real world?
<div style="height:0.75em;"></div>

This is the root of a tree of questions aimed at programmers and non-technical readers wanting to learn the fundamentals of simulation technology and how it can be useful to the world.

So, why simulate real-world systems at all?

The answer in short: simulations can help us discover better actions to take in our decision-making and interrogate the reasoning behind a decision in ways other predictive AI approaches cannot match.

To understand this answer properly, we can build up our understanding in layers.

State partitions and timesteps give us a way to describe how a system evolves in time; these are the fundamental building blocks.

Probabilistic thinking gives us a way to reason about its possible trajectories without enumerating them.

Objectives and learning algorithms give us a way to fit parameters to data.

```{=html}
<style>
  #synth-loop-demo .synth-loop-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.9em;
  }
  @media (max-width: 600px) {
    #synth-loop-demo .synth-loop-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
<div id="synth-loop-demo" style="margin:1.5em 0;padding:1em;background:#ffffff;">
  <div class="synth-loop-grid">
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Decisions</div>
      <svg id="synth-loop-decision-svg" width="100%" height="120" viewBox="0 0 220 120" role="img" aria-label="Current state vs target"></svg>
      <div id="synth-loop-decision-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;line-height:1.4;"></div>
      <div style="font-size:0.9rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">The simulation is run to support a decision.</div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Building blocks</div>
      <svg id="synth-loop-state-svg" width="100%" height="120" viewBox="0 0 220 120" role="img" aria-label="State trajectory"></svg>
      <div id="synth-loop-state-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;line-height:1.4;"></div>
      <div style="font-size:0.9rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Time and state advance one step.</div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Probabilities</div>
      <svg id="synth-loop-prob-svg" width="100%" height="120" viewBox="0 0 220 120" role="img" aria-label="Posterior over theta"></svg>
      <div id="synth-loop-prob-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;line-height:1.4;"></div>
      <div style="font-size:0.9rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">The states have probabilities.</div>
    </div>
    <div style="border:1px solid #2c3e50;border-radius:6px;padding:0.6em;background:#ffffff;">
      <div style="font-weight:600;color:#2c3e50;margin-bottom:0.35em;padding:0 0.75em;">Learning</div>
      <svg id="synth-loop-learn-svg" width="100%" height="120" viewBox="0 0 220 120" role="img" aria-label="Cumulative reward"></svg>
      <div id="synth-loop-learn-text" style="font-size:1rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;line-height:1.4;"></div>
      <div style="font-size:0.9rem;color:#2c3e50;margin-top:0.35em;padding:0 0.75em;">Parameters are updated using those probabilities.</div>
    </div>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:0.75em;align-items:center;justify-content:flex-start;margin-top:0.8em;">
    <button id="synth-loop-advance" type="button" style="cursor:pointer;border:1px solid #3c78d8;background:#3c78d8;color:#ffffff;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Advance one full iteration
    </button>
    <button id="synth-loop-reset" type="button" style="cursor:pointer;border:1px solid #2c3e50;background:#ffffff;color:#2c3e50;padding:0.4em 0.8em;border-radius:6px;font-size:1rem;">
      Reset
    </button>
  </div>
</div>
<script>
(() => {
  const advanceBtn = document.getElementById("synth-loop-advance");
  const resetBtn = document.getElementById("synth-loop-reset");
  if (!advanceBtn || !resetBtn) return;

  const target = 1.5;
  const noiseStd = 0.22;
  const driftScale = 0.35;
  const trueTheta = 1.0;
  const nParticles = 40;
  const maxHistory = 24;

  const createSvgEl = (name, attrs = {}) => {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    return el;
  };
  const randn = () => {
    const u = Math.random(), v = Math.random();
    return Math.sqrt(-2 * Math.log(u || 1e-10)) * Math.cos(2 * Math.PI * v);
  };

  let s;
  const init = () => {
    const particles = [];
    for (let i = 0; i < nParticles; i++) {
      particles.push({ theta: 0.4 + randn() * 0.6, weight: 1 / nParticles });
    }
    s = { t: 0, x: 0, particles, reward: 0, stateHist: [0], rewardHist: [0] };
  };

  const meanTheta = () => s.particles.reduce((acc, p) => acc + p.weight * p.theta, 0);
  const varTheta = () => {
    const m = meanTheta();
    return s.particles.reduce((acc, p) => acc + p.weight * (p.theta - m) ** 2, 0);
  };

  const advance = () => {
    s.t += 1;
    const drift = (target - s.x) * driftScale;
    const dx = trueTheta * drift + randn() * noiseStd;
    s.x += dx;

    let totalW = 0;
    s.particles.forEach(p => {
      const predicted = p.theta * drift;
      const err = dx - predicted;
      p.weight *= Math.exp(-0.5 * (err * err) / (noiseStd * noiseStd));
      totalW += p.weight;
    });
    if (totalW > 0) s.particles.forEach(p => (p.weight /= totalW));

    const ess = 1 / s.particles.reduce((acc, p) => acc + p.weight * p.weight, 0);
    if (ess < nParticles / 3) {
      const cum = []; let c = 0;
      s.particles.forEach(p => { c += p.weight; cum.push(c); });
      const np = []; const u0 = Math.random() / nParticles; let j = 0;
      for (let i = 0; i < nParticles; i++) {
        const u = u0 + i / nParticles;
        while (j < nParticles - 1 && cum[j] < u) j++;
        np.push({ theta: s.particles[j].theta + randn() * 0.04, weight: 1 / nParticles });
      }
      s.particles = np;
    }

    s.reward += -Math.abs(s.x - target);
    s.stateHist.push(s.x);
    s.rewardHist.push(s.reward);
    if (s.stateHist.length > maxHistory) s.stateHist.shift();
    if (s.rewardHist.length > maxHistory) s.rewardHist.shift();
  };

  const drawDecision = () => {
    const svg = document.getElementById("synth-loop-decision-svg");
    if (!svg) return;
    svg.innerHTML = "";
    const w = 220, h = 120, pad = 14;
    const xMin = -0.5, xMax = 2.5;
    const toX = (v) => pad + ((v - xMin) / (xMax - xMin)) * (w - 2 * pad);
    svg.appendChild(createSvgEl("line", { x1: pad, y1: h / 2, x2: w - pad, y2: h / 2, stroke: "#2c3e50", "stroke-width": "1" }));
    const tx = toX(target);
    svg.appendChild(createSvgEl("line", { x1: tx, y1: h / 2 - 16, x2: tx, y2: h / 2 + 16, stroke: "#b0447a", "stroke-width": "2" }));
    const tl = createSvgEl("text", { x: tx, y: h / 2 + 30, fill: "#b0447a", "font-size": "10", "text-anchor": "middle", "font-family": "system-ui,sans-serif" });
    tl.textContent = "target"; svg.appendChild(tl);
    const sx = toX(Math.max(xMin, Math.min(xMax, s.x)));
    svg.appendChild(createSvgEl("circle", { cx: sx, cy: h / 2, r: 5, fill: "#3c78d8" }));
    const sl = createSvgEl("text", { x: sx, y: h / 2 - 12, fill: "#3c78d8", "font-size": "10", "text-anchor": "middle", "font-family": "system-ui,sans-serif" });
    sl.textContent = "state"; svg.appendChild(sl);
  };

  const drawState = () => {
    const svg = document.getElementById("synth-loop-state-svg");
    if (!svg) return;
    svg.innerHTML = "";
    const w = 220, h = 120, pad = 12;
    const n = s.stateHist.length;
    const minV = Math.min(...s.stateHist, target) - 0.2;
    const maxV = Math.max(...s.stateHist, target) + 0.2;
    const toX = (i) => pad + (i / Math.max(n - 1, 1)) * (w - 2 * pad);
    const toY = (v) => h - pad - ((v - minV) / (maxV - minV || 1)) * (h - 2 * pad);
    svg.appendChild(createSvgEl("line", { x1: pad, y1: toY(target), x2: w - pad, y2: toY(target), stroke: "#b0447a", "stroke-width": "1", "stroke-dasharray": "3 3" }));
    if (n > 1) {
      const path = s.stateHist.map((v, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(v)}`).join(" ");
      svg.appendChild(createSvgEl("path", { d: path, fill: "none", stroke: "#3c78d8", "stroke-width": "2" }));
    }
    if (n > 0) {
      svg.appendChild(createSvgEl("circle", { cx: toX(n - 1), cy: toY(s.stateHist[n - 1]), r: 3, fill: "#3c78d8" }));
    }
  };

  const drawProb = () => {
    const svg = document.getElementById("synth-loop-prob-svg");
    if (!svg) return;
    svg.innerHTML = "";
    const w = 220, h = 120, pad = 12;
    const nBins = 14, thetaMin = -1, thetaMax = 2.5;
    const binW = (thetaMax - thetaMin) / nBins;
    const bins = new Array(nBins).fill(0);
    s.particles.forEach(p => {
      const b = Math.floor((p.theta - thetaMin) / binW);
      if (b >= 0 && b < nBins) bins[b] += p.weight;
    });
    const maxBin = Math.max(...bins, 0.01);
    const barW = (w - 2 * pad) / nBins;
    svg.appendChild(createSvgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#2c3e50", "stroke-width": "1" }));
    bins.forEach((b, i) => {
      const barH = (b / maxBin) * (h - 2 * pad);
      if (barH > 0.5) {
        svg.appendChild(createSvgEl("rect", {
          x: pad + i * barW + 1, y: h - pad - barH,
          width: Math.max(barW - 2, 1), height: barH,
          fill: "#3c78d8", opacity: "0.7", rx: "1"
        }));
      }
    });
    const trueX = pad + ((trueTheta - thetaMin) / (thetaMax - thetaMin)) * (w - 2 * pad);
    svg.appendChild(createSvgEl("line", { x1: trueX, y1: pad, x2: trueX, y2: h - pad, stroke: "#b0447a", "stroke-width": "1.5", "stroke-dasharray": "3 3" }));
  };

  const drawLearn = () => {
    const svg = document.getElementById("synth-loop-learn-svg");
    if (!svg) return;
    svg.innerHTML = "";
    const w = 220, h = 120, pad = 12;
    const n = s.rewardHist.length;
    const minV = Math.min(...s.rewardHist, 0);
    const maxV = Math.max(...s.rewardHist, 0);
    const toX = (i) => pad + (i / Math.max(n - 1, 1)) * (w - 2 * pad);
    const toY = (v) => h - pad - ((v - minV) / (maxV - minV || 1)) * (h - 2 * pad);
    svg.appendChild(createSvgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#2c3e50", "stroke-width": "1" }));
    if (n > 1) {
      const path = s.rewardHist.map((v, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(v)}`).join(" ");
      svg.appendChild(createSvgEl("path", { d: path, fill: "none", stroke: "#3c78d8", "stroke-width": "2" }));
    }
  };

  const render = () => {
    const m = meanTheta();
    const sd = Math.sqrt(varTheta());
    drawDecision(); drawState(); drawProb(); drawLearn();
    const dt = document.getElementById("synth-loop-decision-text");
    const st = document.getElementById("synth-loop-state-text");
    const pt = document.getElementById("synth-loop-prob-text");
    const lt = document.getElementById("synth-loop-learn-text");
    if (dt) dt.textContent = "Target = " + target.toFixed(2) + " · gap = " + (target - s.x).toFixed(2);
    if (st) st.textContent = "t = " + s.t + " · state x = " + s.x.toFixed(2);
    if (pt) pt.textContent = "θ uncertainty ≈ ±" + sd.toFixed(2);
    if (lt) lt.textContent = "θ estimate = " + m.toFixed(2) + " · reward = " + s.reward.toFixed(1);
  };

  init(); render();
  advanceBtn.addEventListener("click", () => { advance(); render(); });
  resetBtn.addEventListener("click", () => { init(); render(); });
})();
</script>
```


## References and further reading

::: {#refs}
:::
