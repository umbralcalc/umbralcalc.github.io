---
title: "What is a policy?"
# tag: "How do I automate taking actions with simulations?"
series-blurb: "A collection of posts on ... No maths; just diagrams and straightforward descriptions all the way through."
order: 1
---

# What is a policy?
<div style="height:0.75em;"></div>

## Defining it

Action-taking policies define the logic which take in the state of the world and map it to a taken action at any moment in time.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/what_is_a_policy/action-taking-policy.svg"/></center>

Note that the downstream iteration of simulated 'outcomes' from a given action can be replaced by any kind of downstream simulation that is connected to the action iteration; we only think of it as a single 'iterate simulation partition' here for convenience.

## Sensitivity and generalisation

Which action-taking policy logic finds the best actions?

How sensitive is this choice to changes in the data? How sensitive is this choice to changes in the outcome model?

Answers to both of these questions tell us how the action-taking policy generalises within the problem domain to alternative scenarios and underlying system mechanisms.

How sensitive is this choice to changes in the action parameters?

In much the same way as it does in [learning simulations of the real world](https://umbralcalc.github.io/posts/learning_simulations_of_the_real_world.html) answering this question tells us how _sloppy_ the action-taking policy is, and as a result how generalisable it could be to other problem domains.