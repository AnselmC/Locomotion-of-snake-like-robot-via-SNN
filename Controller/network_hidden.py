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
        self.neuron_hidden_l = nest.Create("iaf_psc_alpha", p.resolution[0]*(p.resolution[1]//4), params=p.iaf_params_hidden)
        self.neuron_hidden_r = nest.Create("iaf_psc_alpha", p.resolution[0]*(p.resolution[1]//4), params=p.iaf_params_hidden)
        # Create motor IAF neurons
        self.neuron_post_l = nest.Create("iaf_psc_alpha", 1, params=p.iaf_params)
        self.neuron_post_r = nest.Create("iaf_psc_alpha", 1, params=p.iaf_params)
        # Create Output spike detectors
        self.spike_detector_l = nest.Create("spike_detector", 1, params={"withtime": True})
        self.spike_detector_r = nest.Create("spike_detector", 1, params={"withtime": True})

        # Create R-STDP synapses
        self.syn_dict = {"model": "stdp_dopamine_synapse",
                        "weight": {"distribution": "uniform", "low": p.w0_min, "high": p.w0_max}}
        self.vt = nest.Create("volume_transmitter")
        nest.SetDefaults("stdp_dopamine_synapse", {"vt": self.vt[0], "tau_c": p.tau_c, "tau_n": p.tau_n, "Wmin": p.w_min, "Wmax": p.w_max, "A_plus": p.A_plus, "A_minus": p.A_minus})
        nest.Connect(self.spike_generators, self.neuron_pre, "one_to_one")
        nest.Connect(self.neuron_pre, self.neuron_hidden_l, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neuron_pre, self.neuron_hidden_r, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neuron_hidden_l, self.neuron_post_l, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neuron_hidden_r, self.neuron_post_r, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neuron_post_l, self.spike_detector_l, "one_to_one")
        nest.Connect(self.neuron_post_r, self.spike_detector_r, "one_to_one")
        # Create connection handles for hidden layer neurons
        self.conn_hidden_l = []
        for i in range (len(self.neuron_hidden_l)):
            self.conn_hidden_l.append(nest.GetConnections(target=[self.neuron_hidden_l[i]]))
        self.conn_hidden_r = []
        for i in range (len(self.neuron_hidden_r)):
            self.conn_hidden_r.append(nest.GetConnections(target=[self.neuron_hidden_r[i]]))
        # Create connection handles for left and right motor neurons
        self.conn_l = nest.GetConnections(target=self.neuron_post_l)
        self.conn_r = nest.GetConnections(target=self.neuron_post_r)

    def simulate(self, image_data, tdm):
        # Get network weights to hidden layer
        weights_l = np.array(nest.GetStatus(self.conn_l, keys="weight"))
        weights_r = np.array(nest.GetStatus(self.conn_r, keys="weight"))

        # Set tdm signal for left and right neuron connections
        nest.SetStatus(self.conn_l, {"n": -tdm})
        nest.SetStatus(self.conn_r, {"n": tdm})

        # Set tdm for hidden layer neuron connections
        for i in range(len(self.conn_hidden_l)):
            nest.SetStatus(self.conn_hidden_l[i], {"n":-tdm})
            nest.SetStatus(self.conn_hidden_r[i], {"n":tdm})

        # Set poisson neuron firing time span
        time = nest.GetKernelStatus("time")
        nest.SetStatus(self.spike_generators, {"origin": time})
        nest.SetStatus(self.spike_generators, {"stop": p.sim_time})
        # Set poisson neuron firing frequency
        image_data = image_data.reshape(image_data.size)
        for i in range(image_data.size):
            rate = image_data[i]/p.max_spikes
            rate = np.clip(rate,0,1)*p.max_poisson_freq
            nest.SetStatus([self.spike_generators[i]], {"rate": rate})
        # Simulate network
        nest.Simulate(p.sim_time)
        # Get left and right output spikes
        n_l = nest.GetStatus(self.spike_detector_l,keys="n_events")[0]
        n_r = nest.GetStatus(self.spike_detector_r,keys="n_events")[0]
        # Reset output spike detector
        nest.SetStatus(self.spike_detector_l, {"n_events": 0})
        nest.SetStatus(self.spike_detector_r, {"n_events": 0})

        return n_l, n_r, weights_l, weights_r

    def run(self, image_data):
        # Set poisson neuron firing time span
        time = nest.GetKernelStatus("time")
        nest.SetStatus(self.spike_generators, {"origin": time})
        nest.SetStatus(self.spike_generators, {"stop": p.sim_time})
        # Set poisson neuron firing frequency
        image_data = image_data.reshape(image_data.size)
        for i in range(image_data.size):
            rate = image_data[i]/p.max_spikes
            rate = np.clip(rate,0,1)*p.max_poisson_freq
            nest.SetStatus([self.spike_generators[i]], {"rate": rate})
        # Run network
        nest.Prepare()
        nest.Run(p.sim_time)
        nest.Cleanup()
        # Get left and right output spikes
        n_l = nest.GetStatus(self.spike_detector_l,keys="n_events")
        n_r = nest.GetStatus(self.spike_detector_r,keys="n_events")
        # Reset output spike detector
        nest.SetStatus(self.spike_detector_l, {"n_events": 0})
        nest.SetStatus(self.spike_detector_r, {"n_events": 0})
        # Get network weights
        return n_l, n_r

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
