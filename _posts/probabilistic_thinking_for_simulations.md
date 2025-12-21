---
title: "Probabilistic thinking for simulations"
tag: "Simulating Real-World Systems as a Programmer"
order: 3
images:
- "/assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg"
- "/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition-region.svg"
---

# Probabilistic thinking for simulations
<div style="height:0.75em;"></div>

## Why do we care?

Probabilities essentially represent sampling all of the possible Trajectories that a simulation could take in Time simultaneously.

<center><img src="../assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg" /></center>

Using this representation for a real-world simulation, there are two important use cases.

The first uses all of the possible Trajectories the simulation can take to represent how likely it is to take them. This makes it possible to create algorithms which learn the most likely Parameters for State Partitions to match real-world Data.

The second uses the Probabilities to represent a model in place of the simulation itself. In the right circumstances, this results in algorithms which are much more efficient than sampling multiple Trajectories.

## Probabilities and regions

Evaluating the Probability of a particular State Partition History, given Parameters and a Cumulative Timesteps History, looks a similar to the Iterate computation. However, in contrast, this computation does _not_ progress forward in Time.

<center><img src="../assets/probabilistic_thinking_for_simulations/evaluate-probability-partition.svg" /></center>

We might also want to evaluate the Probability of Regions which join together possible values that the whole State Partition History can take.

<center><img src="../assets/probabilistic_thinking_for_simulations/possible-region.svg" /></center>

In many situations, it would be impossible to count the all of the possible values in some Regions, but we can still imagine the computation in this way.

<center><img src="../assets/probabilistic_thinking_for_simulations/evaluate-probability-partition-region.svg" /></center>

## Estimating the mean and variance in state

## Estimating state probabilities in time

## Returning to why we care
