---
title: "Preparing a simulation for action-taking"
# tag: "Trusting Actions on Simulated Systems"
series-blurb: "A collection of posts on how we decide whether an action chosen with a simulation can be trusted. Written especially for programmers and non-technical readers wanting to learn about how to take better actions under uncertainty. No maths; just diagrams and straightforward descriptions all the way through."
order: 3
---

# Preparing a simulation for action-taking
<div style="height:0.75em;"></div>

## The two kinds of sensitivity

Data Scientists will often ask the following question about their models: if I change this input, how will my model prediction change?

Let's give a name to this idea, and call it 'prediction sensitivity'.

But the question we were asking at the end of the last post was more aligned with: if I change this input, how will my _taken action_ change?

Let's call this one 'action-taking sensitivity'.

Both questions are referring to 'inputs' when this really means changing one of two things: changing logic/structure or changing parameters.

<!-- Diagram of action-to-outcome iteration upstream to downstream with the labels of the changes and where they refer to -->

If we want to learn parameters which correspond to optimal simulation trajectories, we first need to specify what 'optimal' means.

We do this by defining an objective whose maximum/minimum possible value will be achieved when our goal is met.

For instance, we may define some logic in a state partition iteration of the simulation which replicates taking 'actions' in the real world. This logic can depend on the simulation parameters so that the latter encodes the behaviour quantitatively.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/action-taking.svg"/></center>

Given this setup, a very common goal of interest is then in finding the best actions to take; which is analogous to optimising the parameters of the action-taking state partition iteration. We will refer to these parameters as 'policy parameters'.

But what should be use as an objective?

The 'discounted future reward' is a quantity we can specify that a simulation trajectory will have accumulated into the future, accounting for increasing distance into the future by 'discounting' it gradually with a weighting.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/discounted-future-reward.svg"/></center>

We are using this concept of discounted future reward in the same way that it is used in [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning).

The idea is that, as you go further into the future, the importance of the reward you have accumulated by then is increasingly irrelevant to actions you might take at the present moment.

## Example: Optimising with evolutionary strategies

The [evolutionary strategies](https://en.wikipedia.org/wiki/Evolution_strategy) algorithm can be applied to search future simulation trajectories to find the best set of policy parameters needed to achieve some discounted future reward.

This algorithm relies on sorting the sampled simulation trajectories according to their discounted future rewards and then using the top fraction of these to update the best known policy parameters (and the variance around them) after each timestep.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/optimising-evolutionary-strategies.svg"/></center>

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

Which action-taking policy logic finds the best actions?

How sensitive is this choice to changes in the data? How sensitive is this choice to changes in the outcome model?

Answers to both of these questions tell us how the action-taking policy generalises within the problem domain to alternative scenarios and underlying system mechanisms.

How sensitive is this choice to changes in the action parameters?

In much the same way as it does in [learning simulations of the real world](https://umbralcalc.github.io/posts/learning_simulations_of_the_real_world.html) answering this question tells us how _sloppy_ the action-taking policy is, and as a result how generalisable it could be to other problem domains.

## Explaining why the simulation predicts what it does

Cover these topics:
- past-looking simulation graph analysis
- forward-looking counterfactual analysis: simulation differencing and why SHAP is better
- forward-looking counterfactual analysis: simulation SHAP analysis

## Inferring which simulation to use

Cover these topics:
- Bayesian model selection applied to action-taking is the same as doing causal inference



