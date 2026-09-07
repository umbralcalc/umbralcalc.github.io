---
title: "Preparing a simulation for action-taking"
# tag: "How can I trust the actions I take in simulations?"
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

## Explaining why the simulation predicts what it does

Cover these topics:
- past-looking simulation graph analysis
- forward-looking counterfactual analysis: simulation differencing and why SHAP is better
- forward-looking counterfactual analysis: simulation SHAP analysis

## Inferring which simulation to use

Cover these topics:
- Bayesian model selection applied to action-taking is the same as doing causal inference



