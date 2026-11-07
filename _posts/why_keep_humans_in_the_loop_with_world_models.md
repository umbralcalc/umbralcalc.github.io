---
title: "Why keep humans in the loop with world models?"
tag: "Loose Threads"
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/black_box_ai_is_an_accelerator_paradigm/shape-statistics.svg"
aliases:
- "Why keep humans in the loop with world models?"
cites:
- "[[when_is_data_good_enough_for_black_box_ai]]"
- "[[what_can_a_simulation_do_that_a_prediction_cannot]]"
nocite: |
  @ha2018
---

# Why keep humans in the loop with world models?
<div style="height:0.75em;"></div>

In order to tackle the data environments we described above, it helps to bring as much useful information into the problem as possible. This information could come in the form of inductive biases in the model structure or prior knowledge provided by an expert.

Black box AI at best encodes only generic statistical or architectural inductive biases, but usually lacks the rich, domain‑specific structure that an explicit 'world model' can provide.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/black_box_ai_is_an_accelerator_paradigm/shape-statistics.svg"/></center>

In contrast to black box AI, world models represent the state of the system _separately from the data_. Simulations can be thought of as a kind of world model, for instance.

A true world model should enable sources of information _distinct from the data_ to be included in its prediction, i.e., domain-specific structure with expert interpretation. This is the only clear way to circumvent data limitations.

Humans 'in the loop' can also interrogate their world models to find explanations for their predictions. In this sense, world models can provide _insights_, not just predictive outputs.

## References and further reading

::: {#refs}
:::
