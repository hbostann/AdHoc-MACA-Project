from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
from nodemodel import GenericNode


def main():
  topo = Topology()
  topo.construct_winslab_topology_with_channels(4, GenericNode, GenericChannel)

  topo.start()

  # Send - receive messages
  # keep track of bytes and time to generate statistics.
