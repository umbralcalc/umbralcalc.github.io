---
title: "What is a batch simulation architecture?"
tag: "Loose Threads"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/stepwise-vs-batch.svg"
aliases:
- "What is a batch simulation architecture?"
cites:
- "[[how_do_simulations_run_on_cpus]]"
nocite: |
  @jouppi2017
---

# What is a batch simulation architecture?
<div style="height:0.75em;"></div>

Batch simulation architectures evaluate multiple successive sequences of next state values for the system over a wider interval in time all as one computational block.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/stepwise-vs-batch.svg" width=600/></center>

Despite their appearance, batch simulation architectures cannot fundamentally evaluate the next state values at different timesteps in a truly parallel fashion. Simulations must still preserve the causal relationships between these next state values as they progress in time.

To ensure this causality, some form of iteration can be performed; like the stepwise architecture implies by evaluating it recursively. 

However, it is sometimes sufficient to simply encode the causal/temporal dependencies between state values along the simulation timeline as part of a batch prediction; which is how some machine learning models are used to predict time series data.

## References and further reading

::: {#refs}
:::
