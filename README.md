
# Autonomous Locomotion Control for a Snake-like Robot with a Dynamic Vision Sensor and a Spiking Neural Network

The repository for the Bachelor's Thesis in Informatics 'Autonomous Locomotion Control for a Snake-like Robot with a Dynamic Vision Sensor and a Spiking Neural Network' by Christoph Clement under the supervision of Zhenshan Bing, M.Sc. at the TU Munich.

-- **controller**: Contains the python module for the SNN controlled Locomotion of the snake and plotting scripts for the training Figures.
-- **data**: Contains h5f, csv and json files of the training and testing sessions
-- **plots**: Contains plotting scripts for the testing Figures and other Figures from the thesis and the actual testing and training Figures.
-- **V-REP_scenarios**: Contains the different V-REP scenarios.

## Abstract
How is the brain able to process vast amounts of information so energy efficient? Compared to modern Artificial Neural Networks (ANNs), the energy consumption of the brain is ten times lower - 20W in comparison to 200W. On top of that, we are still far away from imitating the brain's capabilities with ANNs.

A solution to this question might come from the third generation of ANNs - Spiking Neural Networks (SNNs) that mimic the underlying mechanism of the brain better than current ANNs. They incorporate spatial and temporal information into their calculations leading them to be more computationally and energy efficient. Especially in combination with Dynamic Vision Sensors (DVSs), they are a great fit for autonomous robots where energy efficiency and fast real-time computations are key success factors.

In this work, a SNN controller using the Reward-modulated Spike Timing Dependent Plasticity learning rule for the autonomous locomotion control of a snake-like robot is implemented. The controller is trained in a maze environment and demonstrates the ability to cope with new situations in form of different wall heights and maze angles during testing. In a real world application, such a robot could be deployed in areas with uneven terrain like in a collapsed factory building.

## Getting Started

### Prerequisites

 - Ubuntu 16.04 LTS
 - V-REP 3.4.0
 - ROS Kinetic 1.12.13
 - Python 2.7
 - NEST 2.14.0

### Installing

TODO

## Start a training/ testing simulation

1. Start a ROS node via the terminal
	```
	roscore
	```
2. V-REP
- Start V-REP via another terminal from the V-REP foler
	```
	.\vrep.sh
	```
- Open V-REP scenario and start the V-REP simulation
3. SNN
- Set parameters in `./controller/parameters.py`. Create a subfolder for each session otherwise the data will be overwritten.
- Start training/ testing simulation by running `./controller/training.py`/ `./controller/controller.py`.

## License

TODO
