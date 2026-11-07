---
title: "What is a policy?"
draft: true
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_is_a_policy/action-taking-policy.svg"
cites:
- "[[how_do_i_automate_taking_actions_with_simulations]]"
- "[[how_does_an_action_enter_a_simulation]]"
nocite: |
  @suttonbarto2018
---

# What is a policy?
<div style="height:0.75em;"></div>

Action-taking policies define the logic which take in the state of the world and map it to a taken action at any moment in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_is_a_policy/action-taking-policy.svg"/></center>

Note that the downstream iteration of simulated 'outcomes' from a given action can be replaced by any kind of downstream simulation that is connected to the action iteration; we only think of it as a single 'iterate simulation partition' here for convenience.

## References and further reading

::: {#refs}
:::
