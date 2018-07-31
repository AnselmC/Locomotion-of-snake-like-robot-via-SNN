# TODO
- Freeze development, reset data and plots and systematically test hyperparameters with scenario_2_texture_concrete:
  - session_001: baseline
    - episodes:   6
    - steps:      2220
    - vrep_steps: 2452
    - distance:   73.87
  - session_002: higher resolution (/8 instead of /16)    --> learns faster
    - episodes:   1
    - steps:      349
    - vrep_steps: 470
    - distance:   14.65
  - session_003: lower resolution (/32 instead of /16)    --> doesn't learn
  - session_004: max_poisson_freq = 256, max_spikes = 16.
    - episodes:   10
    - steps:      3374
    - vrep_steps: 4527
    - distance:   136.32
  - session_005: w_max = 5000, w_min = -w_max
    - episodes:   5
    - steps:      2244
    - vrep_steps: 2490
    - distance:   75.72
  - session_006: w0_max = 500, w0_min = -w0_max
  - session_007: double reward_factor = 0.0005
  - session_008: half reward_factor = 0.000125
- Testing scenario
- Code rework + comments
  - Snake Lua script remove comments
  - Remove debug comments
- Mark episodes on weights change over time plot
- Add training length in VREP

# Questions
- Turning model
- Feedback Hidden layer idea
- Snake falls through floor
- What metrics to plot in discussion
- getState function Claus
- max_spikes calculation
- Timing analysis, VREP and SNN out of sync
- testing scneario

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
