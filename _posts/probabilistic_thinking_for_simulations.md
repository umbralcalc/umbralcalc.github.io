---
title: "Probabilistic thinking for simulations"
tag: "Simulating Real-World Systems as a Programmer"
order: 4
series-blurb: "A collection of posts on the foundations and patterns for building simulations of the real world. Written especially for programmers and non-technical readers wanting to learn the fundamentals. All written material and non-interactive diagrams were human-generated, where some interactive elements were programmed using generative AI tools."
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition-region.svg"
---

# Probabilistic thinking for simulations
<div style="height:0.75em;"></div>

## Why do we care?

The 'Trajectory' of a simulation is the sequence of possible State Values that its Partitions actually take during a specific Simulation Run.

Probabilities can represent sampling all of the possible Trajectories that a simulation could take in Time, simultaneously.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/probabilites-vs-trajectories.svg" /></center>

Using this representation for a real-world simulation, there are two important use cases.

The first uses all of the possible Trajectories the simulation can take to represent how likely it is to take them. This makes it possible to create algorithms which learn the most likely Parameters for State Partitions to match real-world Data.

The second uses the Probabilities to represent a model in place of the simulation itself. In the right circumstances, this results in algorithms which are much more efficient than sampling multiple Trajectories explicitly.

## Probabilities and regions

Evaluating the Probability of a particular State Partition History, given Parameters and a Cumulative Timesteps History, looks a similar to the Iterate computation. However, in contrast, this computation does _not_ progress forward in Time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition.svg" /></center>

We might also want to evaluate the Probability of Regions which join together possible values that the whole State Partition History can take.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/possible-region.svg" /></center>

In many situations, it would be impossible to count the all of the possible values in some Regions, but we can still imagine the computation in this way.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evaluate-probability-partition-region.svg" /></center>

## Conditional probabilities

We can relate two successive probability evaluations in Time together by making the answer of the second depend on the outcome of the first.

We call the second of these two evaluations a Conditional Probability because its Probability is _conditional_ on the Probability of the first.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/conditional-probability.svg" /></center>

The Probabilities for the whole State Partition History change as the simulation advances in Time by adding the Next State Partition Values into the History.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/evolving-state-partition-history-probability.svg" /></center>

This concept also applies to the Probability of Regions.

Note how this relationship also describes how the Probabilities of State Partition Histories can evolve in Time. One applies the same calculation to the output from the previous one, and so on, recursively.

So why can’t we just use this recursive relationship to model all the trajectories of the simulation at once? For some simpler systems this is indeed possible, but for most simulations in practice this is computationally infeasible.

Think about how one might store the set of all Possible State Partition Histories for a sequence of coin flips, and then how this can proliferate in Time as the simulation advances.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/coin-flips-tree.svg" /></center>

The Possible State Partition Histories grow even though the Possible State Values of a coin flip always remain the same (Heads or Tails).

In practice, for most real-world systems, the set of Possible State Values _also_ grows. To see how this can be the case, consider the Trajectories of a randomly moving point on a simple 2-dimensional grid.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/random-walker-grid.svg" /></center>

## Estimating the probabilities of state values

There is a way we can compute these Probabilities without having to trace the path of every possible Trajectory, and often without having to keep a record of every Possible State Value.

We start by estimating the Statistics of these Probabilities. 

The simplest example of these Statistics is the Estimated Mean State Value. 

The obvious way to calculate this is to take the average State Value for a given Timestep across multiple simulation Trajectories.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/average-across-trajectories.svg" /></center>

But could we get an estimate of Statistics from only one Trajectory? This would save lots of additional Trajectory computation as a result.

Yes! If we have an accurate 'weighting model' for the past values, we can get an Estimated Mean State Value from a weighted average over the full State Partition History.

<Illustrate weighted average from state partition history>

We might also train a Machine Learning model to predict the Statistics of State Values from the full State Partition History as an alternative.

Note that there are situations where using the State Partition Histories from one Trajectory is not equivalent to using multiple Trajectories (see [Ergodicity](https://en.wikipedia.org/wiki/Ergodicity)). But this kind of technical problem can often be mitigated by using some mix of the two methods.

So we have the Statistics, but where have the Probabilities gone?

There are many different types of mathematical formulae or Machine Learning model which can provide a map back from these estimated Statistics into Probabilities of State Values in Time for either one or multiple Trajectories, depending on the right circumstances.

<Normal, Gamma, Binomial, Poisson, Negative Binomial distribution illustrations with statistics>

Using calculations of the estimated Statistics for a single Trajectory from the State Partition History, we can design a 'Probabilistic Sample Weighting' algorithm using the [stochadex simulation engine](https://umbralcalc.github.io/stochadex).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/prob-reweighting-code.svg" /></center>

This algorithm essentially compresses the information held within the State Partition History into a small amount of data in the form of Statistics. It then uses these Statistics to calculate estimated Probabilities for any Possible State Value in Time.

## Returning to why we care

To be continued...
