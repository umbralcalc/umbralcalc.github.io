---
title: When does specialised hardware help?
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/specialised-classical-batch.svg
cites:
  - "[[what_is_a_batch_simulation_architecture]]"
nocite: |
  @jouppi2017
---

# When does specialised hardware help?
<div style="height:0.75em;"></div>

From the perspective of standard CPUs, batch simulation architectures are often designed to evaluate segments of the simulation timeline using specialised classical hardware.

When we talk about 'specialised classical' hardware here, we mean [GPUs](#ref-wiki_gpu), [TPUs](#ref-wiki_tpu), [IPUs](#ref-graphcore_ipu) and other specialised processors based on classical computing principles (as opposed to quantum processors).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/specialised-classical-batch.svg"/></center>

This architecture can be used to reduce the overall processing time taken to complete a simulation run relative to a stepwise equivalent, but there are tradeoffs which mean this isn't always efficient.

GPUs, TPUs, IPUs, etc. all have their limitations. For example, GPUs and TPUs are highly optimised for dense arithmetic operations but struggle with branching control flow. IPUs offer more flexibility for irregular compute patterns and sparse operations, though they still prioritise throughput over the complex sequential logic that CPUs handle well.

So there are basically certain types of simulation algorithm that can be written that GPUs, TPUs, IPUs, etc. are not well-suited to reducing the overall processing time for.

In addition, this specialised hardware typically requires data transfer to/from CPU memory (at the very least for initialisation and final results), which also takes processing time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/processing-time-per-timestep.svg"/></center>

So, when deciding on the number of timesteps a batch simulation architecture should use for the best performance, software engineers must take into account:

- the available memory of their specialised hardware
- the memory requirements for their simulation state partition histories
- the overall number of timesteps they need to perform
- the implications this has on the number of I/O operations needed to interact with CPU memory
- and the implications _this_ has on reducing the overall processing time, given the specialised hardware.

## References and further reading

::: {#refs}
:::
