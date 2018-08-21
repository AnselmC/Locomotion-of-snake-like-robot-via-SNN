# TODO
- Hyperparameter Evalution for scenario_2
  - session_001: Initial configuration
  - session_002: w_max = 10000.
  - session_003: reward_factor = 0.000125
----
  - session_004: w_max = 10000., w_min = -w_max, w0_max = w_min/50, w0_min = w0_max-1, reward_factor = 0.00025

- Code rework + comments
  - Snake Lua script remove comments
  - Remove debug comments
  - Remove pos_data Subscriber in environment
  - Clean Repository
- In Latex
  - (!) Write Abstract
  - List of Figures: show only titles
  - (!) Write Introduction
  - Chapter 2
    - Plot LIF Figure (Figure 2.4)
    - Plot eligibility trace Figure (Figure 2.5)
    - Plot weight update Figure (Figure 2.6)
  - Chapter 3 Methodology
    - Add technical drawing of snake module from Anselm
    - New snake picture (Figure 3.1)
    - New DVS frame (Figure 3.3)
    - New maze picture (Figure 3.4)
    - Controller/ Training flowchart test_length Schrift not correct (Figure 3.6/ Appendix)
    - Revise network architecture figure (16x10 instead of 8x5 pixel)
    - Write Poisson instead of poisson in Figure 3.9a
  - Chapter 4 Discussion
    - Bigger text in Figure 4.1
      - (a): session_007 maze_extended
      - (b): session_001 maze_extended
      - (c): session_001 maze_new_approach
      - (d): session_002 maze_new_approach
    - DVS frame of different scenarios
    - Separate controller performance figure (Figure 4.4)
  - (!) Write Conclusion and Outlook
  - Appendix
    - Check if values in table are correct
  - For all:
    - If two headings are directly beneath each other, an introduction paragraph is missing
    - make subsubsection to subsubsection*

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
- 3 scenarios:

Meeting on 08/31/2018
- Comprehensive story needed
- Goal: Create controller that is indifferent to wall height
- Ideas:
  - Don't use concrete texture but instead a thick line that is always on the same height.
  - Train on scenario with different wall heights
