---
title: "Rugby managers under the microscope"
# tag: "Engineering Smart Actions in Practice"
order: 1
---

# Rugby managers under the microscope
<div style="height:0.75em;"></div>

- trywizard data science project to use it as a way of validating the stochadex analysis package is fit for purpose.
- update article about trywizard with this!
- Goal: Build some decision-making software that helps rugby managers make player substitutions at the best time in the match.
  - Project todos:
    - Manually pull together events/players/team features csvs for each season and use these in the app 
    - Write functions to extract these key features from the data:
      - Carefully smoothed average event rates, grouped by position and time spent on the field (fatigue context), as a function of time for all matches
      - Individual team event rate adjustments to this average, grouped by season (tactics/coaching context)
      - Individual player event rate adjustments, grouped by season (player development/tactical alignment context) to the team-adjusted average
