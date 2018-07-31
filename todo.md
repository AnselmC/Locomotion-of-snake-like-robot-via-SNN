# TODO
- Freeze development, reset data and plots and systematically test hyperparameters with scenario_2_texture_concrete:
  - session_001: baseline
  - session_002: higher resolution (/8 instead of /16)    --> learns faster
  - session_003: lower resolution (/32 instead of /16)    --> doesn't learn
  - session_004: max_poisson_freq = 256, max_spikes = 16.
  - session_005: w_max = 5000, w_min = -w_max
  - session_006: w0_max = 500, w0_min = -w0_max
  - session_006: double reward_factor = 0.0005
  - session_006: half reward_factor = 0.000125
- Testing scenario
- Code rework + comments
  - Snake Lua script remove comments
  - Remove debug comments
- Mark episodes on weights change over time plot

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
