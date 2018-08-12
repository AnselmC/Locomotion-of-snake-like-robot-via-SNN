# TODO

  - session_015: test best of the above with different texture

- Testing scenario
  - Different heights in same scenario
- Code rework + comments
  - Snake Lua script remove comments
  - Remove debug comments
- Add training length in VREP
- In Latex
  - New thesis title
  - Write Abstract
  - List of Figures: show only titles
  - Write Introduction
  - Remove RL chapter
  - Plot LIF Figure (Figure 2.4)
  - Plot eligibility trace Figure (Figure 2.5)
  - Plot weight update Figure (Figure 2.6)
  - Combine Theoretical Background and Literature Review
  - Add nicer picture of the snake (Figure 4.1)
  - Renew DVS frame (Figure 4.3)
  - Add maze picture (Section 4.1.3)
  - Revise controller flowchart (Figure 4.5):
    - Bigger text
    - Run instead of simulate function
  - Own network architecture figure (Figure 4.6)
  - Own reward figure (Figure 4.7)
  - Use network.run() function in Figure 4.8a
  - Revise step function flowchart (Figure 4.8b)
    - Bigger text
    - Check if it is correct
  - For section 5.2.1
    - Add Hyperparameter table
    - Put 3 steps_distance plots into one Figure
  - Add training flowchart
  - Write section 5.2.2 Different heights
    With the above described hyperparameters, three more controllers were trained.
    Besides the one for the scenario with 2m high walls, controllers for a height of 0.5m, 1m and 1.5m were trained in order to determine which of them copes best with different heights during testing.
    Table TODO depicts the steps and travelled distance needed until the snake is able to finish the maze in both direction.
    The steps and distance over episode, weights over steps and final weights plot for the controllers can be found in the ref{appendix} TODO
  - Write section 5.3 Testing
    The four controllers described section TODO are evaluated by testing them with scenarios with different wall heights.
  - Write Conclusion and Outlook

# Questions
- Turning model
- getState function Claus
- max_spikes calculation
- Timing analysis, VREP and SNN out of sync
- testing scenarios
- New thesis Title
- Time (present or past)

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
