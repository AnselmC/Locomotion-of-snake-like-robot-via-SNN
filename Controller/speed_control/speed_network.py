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

        # Create motor IAF neurons
        self.neuron_post = nest.Create("iaf_psc_alpha", 2, params=p.iaf_params)
        # Create Output spike detector
        self.spike_detector = nest.Create("spike_detector", 2, params={"withtime": True})
        # Create R-STDP synapses
        self.syn_dict = {"model": "stdp_dopamine_synapse",
                        "weight": {"distribution": "uniform", "low": p.w0_min, "high": p.w0_max}}
        self.vt = nest.Create("volume_transmitter")
        nest.SetDefaults("stdp_dopamine_synapse", {"vt": self.vt[0], "tau_c": p.tau_c, "tau_n": p.tau_n, "Wmin": p.w_min, "Wmax": p.w_max, "A_plus": p.A_plus, "A_minus": p.A_minus})
        nest.Connect(self.spike_generators, self.neuron_pre, "one_to_one")
        nest.Connect(self.neuron_pre, self.neuron_post, "all_to_all", syn_spec=self.syn_dict)
        nest.Connect(self.neuron_post, self.spike_detector, "one_to_one")
        # Create connection handles for faster and slower motor neurons
        self.conn_faster = nest.GetConnections(target=[self.neuron_post[0]])
        self.conn_slower = nest.GetConnections(target=[self.neuron_post[1]])

    def simulate(self, image_data, sdm):
        # Set tdm signal for faster and slower neuron connections
        nest.SetStatus(self.conn_faster, {"n": -sdm})
        nest.SetStatus(self.conn_slower, {"n": sdm})

        # Set poisson neuron firing time span
        time = nest.GetKernelStatus("time")
        nest.SetStatus(self.spike_generators, {"origin": time})
        nest.SetStatus(self.spike_generators, {"stop": p.sim_time})
        # Set poisson neuron firing frequency
        image_data = image_data.reshape(image_data.size)
        for i in range(image_data.size):
            #print image_data[i]
            rate = image_data[i]/p.max_spikes
            rate = np.clip(rate,0,1)*p.max_poisson_freq
            nest.SetStatus([self.spike_generators[i]], {"rate": rate})
        # Simulate network
        nest.Simulate(p.sim_time)
        # Get faster and slower output spikes
        n_faster = nest.GetStatus(self.spike_detector,keys="n_events")[0]
        n_slower = nest.GetStatus(self.spike_detector,keys="n_events")[1]
        # Reset output spike detector
        nest.SetStatus(self.spike_detector, {"n_events": 0})
        # Get network weights
        weights_faster = np.array(nest.GetStatus(self.conn_faster, keys="weight")).reshape(p.resolution)
        weights_slower = np.array(nest.GetStatus(self.conn_slower, keys="weight")).reshape(p.resolution)

        return n_faster, n_slower, weights_faster, weights_slower

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
        # Get faster and slower output spikes
        n_faster = nest.GetStatus(self.spike_detector,keys="n_events")[0]
        n_slower = nest.GetStatus(self.spike_detector,keys="n_events")[1]
        # Reset output spike detector
        nest.SetStatus(self.spike_detector, {"n_events": 0})
        # Get network weights
        return n_faster, n_slower

    def set_weights(self, weights_faster, weights_slower):
        # Translate weights into dictionary format
        w_faster = []
        for w in weights_faster.reshape(weights_faster.size):
            w_faster.append({'weight': w})
        w_slower = []
        for w in weights_slower.reshape(weights_slower.size):
            w_slower.append({'weight': w})

        nest.SetStatus(self.conn_faster, w_faster)
        nest.SetStatus(self.conn_slower, w_slower)
        return
