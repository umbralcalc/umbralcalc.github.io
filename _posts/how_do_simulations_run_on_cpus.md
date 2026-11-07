---
title: "How do simulations run on CPUs?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-graph-edges.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-stepwise-architectures.svg"
cites:
- "[[what_is_a_simulation_run]]"
- "[[how_are_a_partitions_next_values_calculated]]"
nocite: |
  @lawkelton2014
---

# How do simulations run on CPUs?
<div style="height:0.75em;"></div>

When we talk about 'classical' hardware here, we just mean standard CPUs.

On CPUs, simulation architectures may be constructed out of several ingredients. Loosely speaking, these are: memory, threads, channels between threads, processes and Inter-Process Communication (IPC).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-graph-edges.svg"/></center>

All of these ingredients have their own tradeoffs in performance. But they are all useful in constructing the right simulation architectures to satisfy the right use cases.

One of the main simulation architectures people consider is 'stepwise'. These are simulation architectures which evaluate the next state values for the system at each point in time, in turn.

Stepwise simulation architectures on CPUs are typically more performant when using memory, threads and channels between threads in the right combinations.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-stepwise-architectures.svg" width=600/></center>

In contrast, processes, and IPC in particular, are typically more useful when we consider scaling computations in parallel across multiple non-interacting simulation trajectories (which don't need much IPC). This is because IPC comes with more performance limitations.

## References and further reading

::: {#refs}
:::
