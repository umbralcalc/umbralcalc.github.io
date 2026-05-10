---
title: "Simulation architectures on different hardware"
tag: "Loose Threads"
order: 3
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-graph-edges.svg"
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-stepwise-architectures.svg"
---

# Simulation architectures on different hardware
<div style="height:0.75em;"></div>

## Classical hardware

When we talk about 'classical' hardware here, we just mean standard CPUs.

On CPUs, simulation architectures may be constructed out of several ingredients. Loosely speaking, these are: memory, threads, channels between threads, processes and Inter-Process Communication (IPC).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-graph-edges.svg"/></center>

All of these ingredients have their own tradeoffs in performance. But they are all useful in constructing the right simulation architectures to satisfy the right use cases.

One of the main simulation architectures people consider is 'stepwise'. These are simulation architectures which evaluate the next state values for the system at each point in time, in turn.

Stepwise simulation architectures on CPUs are typically more performant when using memory, threads and channels between threads in the right combinations.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/cpu-stepwise-architectures.svg" width=600/></center>

In contrast, processes, and IPC in particular, are typically more useful when we consider scaling computations in parallel across multiple non-interacting simulation trajectories (which don't need much IPC). This is because IPC comes with more performance limitations.

Batch simulation architectures evaluate multiple successive sequences of next state values for the system over a wider interval in time all as one computational block.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/stepwise-vs-batch.svg" width=600/></center>

Despite their appearance, batch simulation architectures cannot fundamentally evaluate the next state values at different timesteps in a truly parallel fashion. Simulations must still preserve the causal relationships between these next state values as they progress in time.

To ensure this causality, some form of iteration can be performed; like the stepwise architecture implies by evaluating it recursively. 

However, it is sometimes sufficient to simply encode the causal/temporal dependencies between state values along the simulation timeline as part of a batch prediction; which is how some machine learning models are used to predict time series data.

## Specialised classical hardware

From the perspective of standard CPUs, batch simulation architectures are often designed to evaluate segments of the simulation timeline using specialised classical hardware.

When we talk about 'specialised classical' hardware here, we mean [GPUs](https://en.wikipedia.org/wiki/Graphics_processing_unit), [TPUs](https://en.wikipedia.org/wiki/Tensor_Processing_Unit), [IPUs](https://www.graphcore.ai/products/ipu) and other specialised processors based on classical computing principles (as opposed to quantum processors).

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

## Quantum hardware

Note that the concepts in this section are the most likely to change with future advancements in quantum computing.

Quantum hardware seems to naturally fit the batch simulation architecture in the same way that specialised classical hardware does.

In order to utilise this hardware within a given batch evaluation, one would need to:

- prepare the initial state of [qubits](https://en.wikipedia.org/wiki/Qubit)
- encode the state partition histories from CPU memory into these qubits
- run quantum gates which encode the logic for multiple timesteps of the simulation
- entangle the next state values at each timestep with [ancilla qubits](https://en.wikipedia.org/wiki/Ancilla_bit) or rely on the qubits for state partition histories themselves
- and measure these next state values in order to write the data to CPU memory.

Note also that the [no-cloning theorem](https://en.wikipedia.org/wiki/No-cloning_theorem) means we cannot simply copy the qubits which have run the quantum gates; the circuit must run separately for each simulation trajectory.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/quantum-batch.svg"/></center>

Therefore, you only get a [quantum advantage](https://en.wikipedia.org/wiki/Quantum_supremacy) if you can store more than one timestep worth of simulation next state values in qubit memory. 

Otherwise, if you only effectively have one instantaneous timestep of qubit memory to use, the processing time will likely be dominated by I/O writing to and from the qubits during the simulation. This is also known as the [quantum I/O bottleneck](https://ianreppel.org/io-bottleneck-in-quantum-computing/).
