"""Node properties are in this file."""

import random
import logging
from wsn_simu.packet.packet import Packet


class Node(object):
    """Each Node belongs to this class.

    General properties of a node are defined here.
    """

    def __init__(self, node_id, x, y, node_range, battery=100, rank=1,
                 node_type=None, radio_type=None, sensors=None):
        """Inititialising/Defining the node."""
        self.id = node_id
        self.x = x
        self.y = y
        self.range = node_range
        self.battery = battery
        self.type = type

        self.in_range_ids = []
        self.in_range_nodes = []

        self.in_base_range = 0
        # if random.random() * 9.5 > 1:
        self.is_healthy = 1
        # else:
        # self.is_healthy = 0
        self.routing_priority_nodes = []
        self.routing_priority_ids = []

        self.transmitting_to = 0
        self.receiving_from = []
        self.count_receiving_from = 0

        self.sensors = sensors

        self.memory = ""
        self.node_type = node_type
        self.radio_type = radio_type

    def broadcast(self, node_list):
        # Make-do function that finds all other nodes that are in range.
        # A function because nodes can die. Running this function will find out
        # what other nodes are in range of each node.
        """node_list = List of nodes that are part of the network.

        Possible improvements:
        Instead of O(n^2), do something more efficient
        """
        self.in_range_ids = []
        self.in_range_nodes = []

        self.transmitting_to = 0
        self.receiving_from = []
        self.count_receiving_from = 0

        for node in node_list:
            if distance_bw_nodes(self, node) <= (self.range)**2:
                # Checking distances of each node
                if node.is_healthy == 1 and node not in self.in_range_nodes:
                    self.in_range_ids.append(node.id)
                    self.in_range_nodes.append(node)

        return self.in_range_nodes

    def battery_consumed_for_packet(self, packet):
        """Use properties of the packet like size etc.to affect the battery."""
        initial_value = self.battery
        try:
            dist = distance_bw_nodes(self, self.routing_priority_nodes[0][0])
            self.battery -= 0.001 * packet.message_size * dist
            logging.info("%d battery %d", self.id, self.battery)

        except Exception:
            print("Nothing in range")
        return initial_value - self.battery

    def transmit(self, packet, model=None):
        """Transmit a packet to the next node with highest priority.

        node.transmit(packet) transmits a packet to
        the node with the highest priority.
        """
        if self.is_healthy == 1:
            for node in packet.route_node:
                if packet.route_node.count(node) > 1:
                    return 0
            if packet.type == 100:
                if self.in_base_range == 1:
                    packet.route_id.append(0)
                else:
                    node_to = self.routing_priority_nodes[0][0]
                    if self not in node_to.receiving_from:
                        """ Helps in battery consumption.
                        A node receiving from more stuff dies faster."""
                        node_to.receiving_from.append(self)
                        node_to.count_receiving_from += 1

                    node_to.receive(packet)
                    # if model == "high lifetime model":
                    #     self.routing_priority_nodes = self.routing_priority_nodes[1::] + self.routing_priority_nodes[0]
                    #     self.routing_priority_ids = self.routing_priority_ids[1::] + self.routing_priority_ids[0]
                    packet.route_id.append(node_to.id)
                    packet.route_node.append(node_to)
                    return 65
            elif packet.type == 101:
                # packet.route_id.append(self.id)
                # packet.route_node.append(self)
                packet.destination.receive(packet)
                return 65

        else:
            # node_list.append(BaseStation(0, centre_x[k], centre_y[k], node_range))
            print(self.id, "node is dead")
            return 65

    def receive(self, packet):
        """Receive a packet from another node."""
        if packet.type == 101:
            # print(packet.route_id)
            return 0
        elif packet.type == 100:
            self.transmit(Packet(101, self.id, self, 3, "ack",
                          destination=packet.route_node[-1]))
            return 1

    def stop_transmitting_to(self, node):
        """Remove self from the path of node."""
        node.receiving_from.remove(self)
        node.count_receiving_from -= 1
        self.transmitting_to = 0

    def stop_receiving_from(self, node):
        """Remove a node from self's neighbours."""
        self.receiving_from.remove(node)
        self.count_receiving_from -= 1
        node.transmitting_to = 0

    def get_sensed_values(self):
        """Get all sensed values."""
        for sensor in self.sensors:
            print(sensor.values)


class BaseStation(Node):
    """Class that describes the base station.

    Only one base station exists in a wireless sensor network.
    Has the same properties as a node.
    """

    def __init__(self, node_id, x, y, node_range):
        """Inititialising the node values of the base station."""
        # Defining the base station
        Node.__init__(self, node_id, x, y, node_range)
        self.id = node_id
        self.x = x
        self.y = y
        self.range = node_range


def distance_bw_nodes(node1, node2):
    """Find the distance between node1 and node2."""
    return (node1.x - node2.x)**2 + (node1.y - node2.y)**2
