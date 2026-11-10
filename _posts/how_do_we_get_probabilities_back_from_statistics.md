---
title: How do we get probabilities back from statistics?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/distributions.svg
cites:
- "[[can_one_trajectory_be_enough_to_estimate_statistics]]"
- "[[how_do_we_estimate_statistics_across_trajectories]]"
nocite: |
  @sarkka2013, @doucet2011
---

# How do we get probabilities back from statistics?
<div style="height:0.75em;"></div>

Through a model that maps estimated statistics back onto probabilities of state values.

There are many different types of mathematical formulae or machine learning model which can provide a map back from these estimated statistics into probabilities of state values in time for either one or multiple trajectories, depending on the right circumstances.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/distributions.svg" /></center>

Using calculations of the estimated statistics for a single trajectory from the state partition history, we can design a 'probabilistic sample weighting' algorithm which compresses the information held within the state partition history into a small amount of data (the statistics).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/probabilistic_thinking_for_simulations/prob-reweighting.svg" /></center>

We can then use these statistics to calculate estimated probabilities for any possible state value in time.

## References and further reading

::: {#refs}
:::
