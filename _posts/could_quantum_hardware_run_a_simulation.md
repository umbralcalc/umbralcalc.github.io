---
title: "Could quantum hardware run a simulation?"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/quantum-batch.svg"
cites:
- "[[what_is_a_batch_simulation_architecture]]"
nocite: |
  @feynman1982, @lloyd1996, @preskill2018, @aaronson2015, @arute2019, @nielsenchuang2010
---

# Could quantum hardware run a simulation?
<div style="height:0.75em;"></div>

In principle yes, as a batch architecture, but with an advantage only if more than one timestep's worth of state fits in qubit memory. The ideas here are the ones on this blog most likely to change with future advancements in quantum computing.

Quantum hardware seems to naturally fit the batch simulation architecture in the same way that specialised classical hardware does.

In order to utilise this hardware within a given batch evaluation, one would need to:

- prepare the initial state of [qubits](#ref-wiki_qubit)
- encode the state partition histories from CPU memory into these qubits
- run quantum gates which encode the logic for multiple timesteps of the simulation
- entangle the next state values at each timestep with [ancilla qubits](#ref-wiki_ancilla_bit) or rely on the qubits for state partition histories themselves
- and measure these next state values in order to write the data to CPU memory.

Note also that the [no-cloning theorem](#ref-wiki_no_cloning) means we cannot simply copy the qubits which have run the quantum gates; the circuit must run separately for each simulation trajectory.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/simulation_architectures_on_different_hardware/quantum-batch.svg"/></center>

Therefore, you only get a [quantum advantage](#ref-wiki_quantum_supremacy) if you can store more than one timestep worth of simulation next state values in qubit memory. 

Otherwise, if you only effectively have one instantaneous timestep of qubit memory to use, the processing time will likely be dominated by I/O writing to and from the qubits during the simulation. This is also known as the [quantum I/O bottleneck](#ref-reppel2023io).

## References and further reading

::: {#refs}
:::
