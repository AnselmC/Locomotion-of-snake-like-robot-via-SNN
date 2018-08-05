# TODO
- Train controller on different wall heights and test it on other heights
  - session_010: train on scenario_2
    - test on scenario_0_1
    - test on scenario_1
    - test on scenario_1_5
    - test on scenario_2
    - test on scenario_3
  - session_011: train on scenario_0_1
    - test on scenario_0_1
    - test on scenario_1
    - test on scenario_1_5
    - test on scenario_2
    - test on scenario_3
  - session_012: train on scenario_1
    - test on scenario_0_1
    - test on scenario_1
    - test on scenario_1_5
    - test on scenario_2
    - test on scenario_3
  - session_013: train on scenario_1_5
    - test on scenario_0_1
    - test on scenario_1
    - test on scenario_1_5
    - test on scenario_2
    - test on scenario_3
  - session_014: train on scenario_3
    - test on scenario_0_1
    - test on scenario_1
    - test on scenario_1_5
    - test on scenario_2
    - test on scenario_3
  - session_015: test best of the above with different texture

- Testing scenario
  - Different wall heights: 0.1m, 1m, 1.5m, 2m, 3m
  - Different heights in same scenario
- Code rework + comments
  - Snake Lua script remove comments
  - Remove debug comments
- Add training length in VREP
- In Latex
  - Revise flowcharts: implementation changes, bigger texts
  - Training flowchart based on controller
  - Matplotlib plots
  - Better Snake Figure
  - Hyperparameter evaluation Figures
  - Maze Figure
  - Abstract
  - Intro
  - Conclusion

# Questions
- Turning model
- Feedback Hidden layer idea
- Snake falls through floor
- What metrics to plot in discussion
  - cumulative reward/ error
- getState function Claus
- max_spikes calculation
- Timing analysis, VREP and SNN out of sync
- testing scenario
  - height of the wall
  - texture of the walls
  - QR Code to mark the boundary

Meeting on 07/20/2018
- Title: Don't mention DVS
- Background
  - Theoretical Background
  - Related Network: more latest research
- Plot graphs by yourself
- Make Snake picture more elegant
- Make flowchart text bigger
- 3 scenarios:
- Theory contribution: Hidden layer with reward backpropagation

Meeting on 07/31/2018
