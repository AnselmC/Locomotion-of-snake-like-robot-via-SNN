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
        self.neurons_input = nest.Create("parrot_neuron", p.resolution[0]*p.resolution[1])
        # Create hidden IAF neurons
        self.neurons_hidden = nest.Create("iaf_psc_alpha", 4, params=p.iaf_params_hidden)
        # Create motor IAF neurons
        self.neurons_output = nest.Create("iaf_psc_alpha", 2, params=p.iaf_params)
        # Create Output spike detector
        self.spike_detector = nest.Create("spike_detector", 2, params={"withtime": True})
        # Create R-STDP synapses
        self.syn_dict = {"model": "stdp_dopamine_synapse",
                        "weight": {"distribution": "uniform", "low": p.w0_min, "high": p.w0_max}}
        self.vt = nest.Create("volume_transmitter")
        nest.SetDefaults("stdp_dopamine_synapse", {"vt": self.vt[0], "tau_c": p.tau_c, "tau_n": p.tau_n, "Wmin": p.w_min, "Wmax": p.w_max, "A_plus": p.A_plus, "A_minus": p.A_minus})
        nest.Connect(self.spike_generators, self.neurons_input, "one_to_one")
        nest.Connect(self.neurons_input, self.neurons_hidden, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neurons_hidden, self.neurons_output, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neurons_output, self.spike_detector, "one_to_one")

        # Create connection handles for left and right motor neuron
        self.conn_hidden = []
        for i in range (len(self.neurons_hidden)):
            self.conn_hidden.append(nest.GetConnections(target=[self.neurons_hidden[i]]))

        self.conn_l = nest.GetConnections(target=[self.neurons_output[0]])
        self.conn_r = nest.GetConnections(target=[self.neurons_output[1]])

    def simulate(self, dvs_data, reward):
        # Get network weights
        weights_l = np.array(nest.GetStatus(self.conn_l, keys="weight"))
        weights_r = np.array(nest.GetStatus(self.conn_r, keys="weight"))
        # Set reward signal for hidden, left and right synapses
        for i in range(len(self.conn_hidden)):
            nest.SetStatus(self.conn_hidden[i], {"n":
                    (-reward*p.reward_factor*weights_l[i] +
                    reward*p.reward_factor*weights_r[i]}))/
                    (weights_l[i] + weights_r[i])

        nest.SetStatus(self.conn_l, {"n": -reward*p.reward_factor})
        nest.SetStatus(self.conn_r, {"n": reward*p.reward_factor})

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
        # Reset output spike detector
        nest.SetStatus(self.spike_detector, {"n_events": 0})
        # Get network weights
        # weights_l = np.array(nest.GetStatus(self.conn_l, keys="weight")).reshape(p.resolution)
        # weights_r = np.array(nest.GetStatus(self.conn_r, keys="weight")).reshape(p.resolution)
        weights_l = np.array(nest.GetStatus(self.conn_l, keys="weight"))
        weights_r = np.array(nest.GetStatus(self.conn_r, keys="weight"))
        return n_l, n_r, weights_l, weights_r

    def set_weights(self, weights_l, weights_r):
        # Translate weights into dictionary format
        w_l = []
        for w in weights_l.reshape(weights_l.size):
            w_l.append({'weight': w})
        w_r = []
        for w in weights_r.reshape(weights_r.size):
            w_r.append({'weight': w})
        # Set left and right network weights
        nest.SetStatus(self.conn_l, w_l)
        nest.SetStatus(self.conn_r, w_r)
        return
