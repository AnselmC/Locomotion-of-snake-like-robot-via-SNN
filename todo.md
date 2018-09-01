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
  - Clean Repository
  - Move plot modules into plots, scenario modules into scenario, ...
- Ask TUM about title change
- In Latex
  - (!) Write Abstract
  - Revise Introduction
  - Chapter 2
    - Caption LIF Figure (Figure 2.3)
    - Caption rstdp Figure (Figure 2.5)
  - Chapter 3 Methodology
    - Nicer floor in maze_perspective Figure
    - Change Network Weights in Network Architecture Figure
    - Replace 45 deg with 135 deg
  - Chapter 4 Discussion
    - Right Weights more influence explanation
    - Add vertical lines to mark section in distance over steps plots
    - For the different wall heights test: plot paths in dimensions figure
    - For the zig_zag maze: add to discussion
    - For the cross mazes:
      - plot paths in dimensions figure
  - (!) Write Conclusion and Outlook
  - For all:
    - If two headings are directly beneath each other, an introduction paragraph is missing
    - make subsubsection to subsubsection*
    - Check Acronyms (First acrfull, then acrshort)
    - Make text of figures as big as description
    - Check sharelatex warnings

# Questions
- Turning model

2. Zig zag test
3. Wall heights test
4. Cross plots
3. Wall heights in dimensions plot
4. Vertical lines in distance plots
