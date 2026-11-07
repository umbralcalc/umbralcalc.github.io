---
title: "What is discounted future reward?"
draft: true
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_optimal_policies_with_the_simulation_itself/discounted-future-reward.svg"
aliases:
- "What is discounted future reward?"
cites:
- "[[how_do_i_automate_taking_actions_with_simulations]]"
- "[[how_do_i_set_up_a_simulation_to_learn_a_policy]]"
nocite: |
  @suttonbarto2018
---

# What is discounted future reward?
<div style="height:0.75em;"></div>

The 'discounted future reward' is a quantity we can specify that a simulation trajectory will have accumulated into the future, accounting for increasing distance into the future by 'discounting' it gradually with a weighting.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/learning_optimal_policies_with_the_simulation_itself/discounted-future-reward.svg"/></center>

We are using this concept of discounted future reward in the same way that it is used in [reinforcement learning](#ref-wiki_reinforcement_learning).

The idea is that, as you go further into the future, the importance of the reward you have accumulated by then is increasingly irrelevant to actions you might take at the present moment.

## References and further reading

::: {#refs}
:::
