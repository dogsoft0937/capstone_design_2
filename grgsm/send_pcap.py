# send_pcap.py
from gnuradio import gr, blocks
from grgsm import gsm_gmsk_mod
from osmosdr import sink

class TransmitFlowgraph(gr.top_block):
    def __init__(self, pcap_file, samp_rate=1e6, freq=947.6e6, gain=40):
        gr.top_block.__init__(self)

        self.source = blocks.file_source(gr.sizeof_gr_complex, pcap_file, False)
        self.sink = sink(args="numchan=1")
        self.sink.set_sample_rate(samp_rate)
        self.sink.set_center_freq(freq)
        self.sink.set_gain(gain)

        self.connect(self.source, self.sink)

if __name__ == '__main__':
    pcap_path = "/root/location_update.pcap"
    tb = TransmitFlowgraph(pcap_path)
    tb.run()
