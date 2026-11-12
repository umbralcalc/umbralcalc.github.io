---
title: How do I automate taking actions with simulations?
nocite: |
  @suttonbarto2018, @powell2022
---

# How do I automate taking actions with simulations?
<div style="height:0.75em;"></div>

By learning the rules or action-taking behaviours you would follow as code, and then using simulations to stress test this code.

The fuller answer to this question requires a few new concepts, the first of which is a 'policy': the logic which takes in the state of the world at any moment and returns the action to take.

Automating a decision then means learning a policy. In the literature this is the language of sequential decision-making and reinforcement learning.

To find a good policy, we need to first find out what 'good' even means. Defining this through 'rewards' is common practice.

It's important to note that not every decision should be automated. How often actions are taken, what regulation demands, and what is ethically at stake all determine how far a policy should act on its own, and whether or not there should be humans in-the-loop anyway.

## References and further reading

::: {#refs}
:::
