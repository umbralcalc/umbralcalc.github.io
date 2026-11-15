---
title: Is there a structure to agent-accelerated work?
nocite: |
  @horvitz1999, @christiano2017, @galbraith1974, @bainbridge1983, @brynjolfsson2025, @larmanbasili2003
cites:
  - "[[is_black_box_ai_an_accelerator]]"
images:
  - https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/umbralcalculations/aligner-implementer.svg
---

# Is there a structure to agent-accelerated work?
<div style="height:0.75em;"></div>

We can separate roles in any piece of work into two distinct categories: the 'aligner' and the 'implementer'. Economists would call these the ['principal' and the 'agent'](#ref-jensenmeckling1976), but since 'agent' is about to mean something else here, we will keep the names above.

The aligner is responsible for what the work the implementer is doing is seeking to accomplish. While this sounds like something static, in reality it is very common for the aligner to [adapt short-term goals as more information is learned](#ref-argyrisschon1978) to keep on track towards a longer-term goal.

The implementer is responsible for doing things towards reaching the goal specified by the aligner. This might involve writing code or doing research, and the outputs from the implementation process result in learning more information that the aligner can use.

AI-accelerated work typically involves [replacing this implementer role with an AI agent](#ref-parasuraman2000), while retaining a [human aligner](#ref-hadfieldmenell2016).

These two symbiotic roles appear everywhere in [human organisations](#ref-jensenmeckling1976), e.g., the manager and the employee or the product manager and tech lead, but how do these roles work together?

There are many models for the interactions between these roles in the literature. Here we will pick one of the simplest possible: where an exchange of information between these roles is mediated by one side [asking a question and the other answering it](#ref-clarkbrennan1991).

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/umbralcalculations/aligner-implementer.svg"/></center>

Different projects will carry different levels of [uncertainty and risk](#ref-knight1921) in what each role should be doing.

Note how the questions should flow towards the direction where this [uncertainty is greatest](#ref-lindley1956) at any point in time. Statisticians know this rule as choosing the question with the greatest 'expected information gain', and machine learners as ['active learning'](#ref-mackay1992).

## References and further reading

::: {#refs}
:::
