---
title: "Preparing a simulation for action-taking"
# tag: "How can I trust the actions I take in simulations?"
series-blurb: "A collection of posts on how we decide whether an action chosen with a simulation can be trusted. Written especially for programmers and non-technical readers wanting to learn about how to take better actions under uncertainty, while trusting the tools they use to help take them. No maths; just diagrams and straightforward descriptions all the way through."
order: 3
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/changing-parameters.svg"
---

# Preparing a simulation for action-taking
<div style="height:0.75em;"></div>

## The two kinds of sensitivity

Data Scientists will often ask the following question: if I change this model or its parameters, how will my prediction change?

We discussed the same idea for simulations in [this post](https://umbralcalc.github.io/posts/learning_simulations_of_the_real_world.html). So let's give a name to this idea, and call it 'prediction sensitivity'.

But the question we were asking at the end of the last post was more aligned with: if I change this model (simulation) or its parameters, how will my _taken action_ change?

Let's call this one 'action-taking sensitivity'.

When we change the parameters of a simulation, its iteration at the same point in time may produce different outcomes, depending on the system state and its history (which may also have changed due to previous iterations in time being different).

<center><img src=https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/changing-parameters.svg /></center>

Similarly, when we change the simulation itself, its iteration at the same point in time may also produce different outcomes.

<center><img src=https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/preparing_a_simulation_for_action_taking/changing-simulation.svg /></center>

In both cases, the simulated outcomes help us to determine which action to take, but in order to do this we need to define what outcomes we are targeting in the first place.

## Explaining why the simulation predicts what it does

Cover these topics:
- past-looking simulation graph analysis
- forward-looking counterfactual analysis: simulation differencing and why SHAP is better
- forward-looking counterfactual analysis: simulation SHAP analysis

## Inferring which simulation to use

Cover these topics:
- Bayesian model selection applied to action-taking is the same as doing causal inference



