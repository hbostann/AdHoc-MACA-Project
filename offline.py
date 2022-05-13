import random
import time
import logging
import sys
import string

from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import \
    GenericChannel

from nodemodel.GenericNode import GenericNode

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
  topo = Topology()
  topo.construct_winslab_topology_with_channels(4, GenericNode, GenericChannel)

  topo.start()
  start = time.time()
  for i in range(5):
    from_id = random.randint(0, 3)
    dest_id = random.randint(0, 3)
    message = "".join(
        random.choices(string.ascii_lowercase, k=random.randint(20, 50)))
    topo.nodes[from_id].SendMessage(dest_id, message)
    time.sleep(0.01)
  end = time.time()
  total_bytes = 0
  for node in topo.nodes.values():
    total_bytes += node.application.received_bytes

  throughput = total_bytes / (end - start)
  print("Throuughput:", throughput / 1000, "(kbps)")
  # Send - receive messages
  # keep track of bytes and time to generate statistics.


if __name__ == '__main__':
  main()
