#!/usr/bin/env python

import nest
import numpy as np
import pylab
import parameters as p

class SpikingNeuralNetwork():
    def __init__(self):
        # NEST options
        np.set_printoptions(precision=1)
        nest.set_verbosity('M_WARNING')
        nest.ResetKernel()
        nest.SetKernelStatus({"local_num_threads" : 1, "resolution" : p.time_resolution})
        # Create Poisson neurons
        self.spike_generators = nest.Create("poisson_generator", p.resolution[0]*p.resolution[1], params=p.poisson_params)
        self.neuron_pre = nest.Create("parrot_neuron", p.resolution[0]*p.resolution[1])
        # Create hidden layer
        self.neuron_hidden = nest.Create("iaf_psc_alpha", (p.resolution[0]//2)*p.resolution[1], params=p.iaf_params)
        # Create motor IAF neurons
        self.neuron_post = nest.Create("iaf_psc_alpha", 4, params=p.iaf_params)
        # Create Output spike detector
        self.spike_detector = nest.Create("spike_detector", 4, params={"withtime": True})
        # Create R-STDP synapses
        self.syn_dict = {"model": "stdp_dopamine_synapse",
                        "weight": {"distribution": "uniform", "low": p.w0_min, "high": p.w0_max}}
        self.vt = nest.Create("volume_transmitter")
        nest.SetDefaults("stdp_dopamine_synapse", {"vt": self.vt[0], "tau_c": p.tau_c, "tau_n": p.tau_n, "Wmin": p.w_min, "Wmax": p.w_max, "A_plus": p.A_plus, "A_minus": p.A_minus})
        nest.Connect(self.spike_generators, self.neuron_pre, "one_to_one")
        nest.Connect(self.neuron_pre, self.neuron_post, "all_to_all", syn_spec=self.syn_dict)
        # nest.Connect(self.neuron_hidden, self.neuron_post, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neuron_post, self.spike_detector, "one_to_one")
        # Create connection handles for hidden layer neurons
        self.conn_hidden = []
        for i in range (len(self.neuron_hidden)):
            self.conn_hidden.append(nest.GetConnections(target=[self.neuron_hidden[i]]))
        # Create connection handles for left and right motor neurons
        self.conn_l = nest.GetConnections(target=[self.neuron_post[0]])
        self.conn_r = nest.GetConnections(target=[self.neuron_post[1]])
        # Create connection handles for slower and faster neurons
        self.conn_slower = nest.GetConnections(target=[self.neuron_post[2]])
        self.conn_faster = nest.GetConnections(target=[self.neuron_post[3]])

    def simulate(self, dvs_data, reward, speed_reward):
        # Set reward for hidden layer neuron connections
        # for i in range(len(self.conn_hidden)):
        #     nest.SetStatus(self.conn_hidden[i], {"n":})

        # Set reward signal for left and right neuron connections
        nest.SetStatus(self.conn_l, {"n": -reward*p.reward_factor})
        nest.SetStatus(self.conn_r, {"n": reward*p.reward_factor})

        # Set reward signal for faster and slower neuron connections
        nest.SetStatus(self.conn_faster, {"n": -speed_reward*p.reward_factor_speed})
        nest.SetStatus(self.conn_slower, {"n": speed_reward*p.reward_factor_speed})
        # Set poisson neuron firing time span
        time = nest.GetKernelStatus("time")
        nest.SetStatus(self.spike_generators, {"origin": time})
        nest.SetStatus(self.spike_generators, {"stop": p.sim_time})
        # Set poisson neuron firing frequency
        dvs_data = dvs_data.reshape(dvs_data.size)
        for i in range(dvs_data.size):
            rate = dvs_data[i]/p.max_spikes
            rate = np.clip(rate,0,1)*p.max_poisson_freq
            nest.SetStatus([self.spike_generators[i]], {"rate": rate})
        # Simulate network
        nest.Simulate(p.sim_time)
        # Get left and right output spikes
        n_l = nest.GetStatus(self.spike_detector,keys="n_events")[0]
        n_r = nest.GetStatus(self.spike_detector,keys="n_events")[1]
        n_slower = nest.GetStatus(self.spike_detector,keys="n_events")[2]
        n_faster = nest.GetStatus(self.spike_detector,keys="n_events")[3]
        # Reset output spike detector
        nest.SetStatus(self.spike_detector, {"n_events": 0})
        # Get network weights
        weights_l = np.array(nest.GetStatus(self.conn_l, keys="weight")).reshape((p.resolution[0])*p.resolution[1])
        weights_r = np.array(nest.GetStatus(self.conn_r, keys="weight")).reshape((p.resolution[0])*p.resolution[1])
        weights_faster = np.array(nest.GetStatus(self.conn_faster, keys="weight")).reshape((p.resolution[0])*p.resolution[1])
        weights_slower = np.array(nest.GetStatus(self.conn_slower, keys="weight")).reshape((p.resolution[0])*p.resolution[1])
        return n_l, n_r, n_slower, n_faster, weights_l, weights_r, weights_slower, weights_faster

    def set_weights(self, weights_l, weights_r, weights_slower, weights_faster):
        # Translate weights into dictionary format
        w_l = []
        for w in weights_l.reshape(weights_l.size):
            w_l.append({'weight': w})
        w_r = []
        for w in weights_r.reshape(weights_r.size):
            w_r.append({'weight': w})
        w_slower = []
        for w in weights_slower.reshape(weights_slower.size):
            w_slower.append({'weight':w})
        w_faster = []
        for w in weights_faster.reshape(weights_faster.size):
            w_faster.append({'weight':w})
        # Set left and right network weights
        nest.SetStatus(self.conn_l, w_l)
        nest.SetStatus(self.conn_r, w_r)
        nest.SetStatus(self.conn_slower, w_slower)
        nest.SetStatus(self.conn_faster, w_faster)
        return