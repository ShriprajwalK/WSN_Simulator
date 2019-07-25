"""A Wireless Sensor Network Simulator to simulate Wireless Sensor Networks."""

import pandas as pd
import sys
import seaborn as sns
import random
# sys.path.append('C:\\Users\Anish\Desktop\MLab\MADHOC\Sim_TBD')

from wsn_simu.node.node import Node, BaseStation, distance_bw_nodes
from wsn_simu.node.hexagonal_model import calculate_o, calculate_p
from wsn_simu.node.hexagonal_model import generate_hex_mesh, draw_ring
from wsn_simu.node.hexagonal_model import hexagonal_lattice_graph
from wsn_simu.node.hexagonal_model import generate_centers
from wsn_simu.packet.packet import Packet
from wsn_simu.sensors.sensors import Sensor



try:
    import matplotlib.pyplot as plt
    import numpy as np
    import operator
    # import time
    import sys

except Exception:
    print("Dependencies not installed")
    print("Dependencies not installed")


plt.close()  # To close any other plt windows just in case


class Network(object):
    """Simulate the network using everything else in the code.

    Network definition, initialising and lifetime etcetra are calculated.
    """

    def __init__(self, length_of_area, breadth_of_area, model=None,
                 node_properties=None, node_id=None, x=None, y=None,
                 frequency=1):
        """Init Network. Defining the network and stuff."""
        self.length_of_area = length_of_area
        self.breadth_of_area = breadth_of_area
        self.model = model
        self.node_properties = node_properties
        self.node_id = node_id
        self.x = x
        self.y = y
        self.frequency = frequency

        self.node_list = []

    def define(self):
        """Define a network. Returns a node_list."""
        if self.model is None:
            self.number_of_nodes = len(self.node_id)
            for i in range(self.number_of_nodes):
                self.node_list.append(Node(self.node_id[i], self.x[i],
                                           self.y[i], self.node_properties[1]))
                # Appending the nodes to the list

        elif self.model == "low latency model":
            self.node_list = low_latency_model(self.node_properties[1],
                                               self.length_of_area,
                                               self.breadth_of_area,)

            for node in self.node_list:
                node.type = self.node_properties[0]

        elif self.model == "high lifetime model":
            # l, b are length and breadth.
            self.node_list = high_lifetime_model(self.node_properties[1],
                                                 self.length_of_area,
                                                 self.breadth_of_area)

        elif self.model == "high reliability model":
            # l, b are length and breadth.
            self.node_list = high_reliability_model(self.node_properties[1],
                                                 self.length_of_area,
                                                 self.breadth_of_area)


        return self.node_list

    def initialize(self):
        """Do these as soon as a network is defined."""
        for node in self.node_list:
            node.broadcast(self.node_list)
        self.in_sink_range = self.node_list[-1].broadcast(self.node_list[-2::-1])
        for node in self.in_sink_range:
            node.in_range_nodes.append(self.node_list[-1])
            node.in_range_ids.append(0)
            node.in_base_range = 1

        return self.node_list

    def is_alive(self):
        """Check if the network is alive."""
        alive = False
        for node in self.node_list:
            if node.in_base_range == 1:
                if node.is_healthy == 1:
                    alive = alive or True

        return alive


def distance_of_nodes(node_list):
    """Return a dict containing distance b/w nodes and sink nodes."""
    distance_dict = {}
    for node in node_list:
        distance_dict[node] = distance_bw_nodes(node_list[-1], node)
    return distance_dict


def draw_packets(packet_list):
    """Plot the route taken by the packet."""
    x = np.linspace(0, 45, 1000)
    for packet in packet_list:
        for i in range(len(packet.route_node)):
            if i < (len(packet.route_node) - 1):
                # to_node = route_node[i+1]
                # from_node = route_node[i]
                # plt.plot(x,(packet.to_node.y -
                # packet.from_node.y)/
                # (packet.to_node.x-packet.from_node.x)*x, '--c')
                # plt.xlim(to_node.x, from_node.x)
                # plt.ylim(to_node.y, from_node.y)
                plt.plot(x, x + 1, '--c')
    plt.show()


def draw_figure(length, breadth, node_list, base):
    """Draw the whole network."""
    fig = plt.figure()  # plt stuff that seem to be a must to draw circles.
    ax = fig.add_subplot(1, 1, 1)
    # Base station radius

    for node in node_list[:-1:]:
        if node.is_healthy == 1:
            plt.scatter(node.x, node.y)  # Plotting the nodes

            plt.plot([0, length, length, 0, 0], [0, 0, breadth, breadth, 0])
            node_range = plt.Circle((node.x, node.y), node.range, fill=False)
            # Plotting the circle for each node
            plt.gca().set_aspect('equal')  # making x-axis and y-axis equal
            # Trying to display id numbers on the nodes:
            ax.annotate(node.id, (node.x, node.y))
            # Displaying node ids along with the nodes on the graph
            # ax.add_patch(node_range)  # Finally drawing the circle.

    if base is True:
        plt.scatter(node_list[-1].x, node_list[-1].y)
        base_range = plt.Circle((node_list[-1].x, node_list[-1].y),
                                node_list[-1].range, fill=False, color="b")

        ax.annotate("sink node", (node_list[-1].x, node_list[-1].y))
        ax.add_patch(base_range)  # Adding the circle base_range to the figure
    plt.title("Simulator plot")
    plt.xlabel("Breadth of given area")
    plt.ylabel("Length of given area")

    plt.show()


def low_latency_model(node_range, length_of_area, breadth_of_area):
    """Model for relatively low latency.

    Placing nodes such that the number of jumps are the least
    at a moderate cost.
    """
    node_list = []
    node_id = 1
    initial_value = node_range / np.sqrt(2) # - 5
    num_nodes_along_length = int(length_of_area / initial_value)
    num_nodes_along_breadth = int(breadth_of_area / initial_value)

    for i in range(num_nodes_along_length + 1): # + 1
        for j in range(num_nodes_along_breadth + 1): # + 1
            node_list.append(Node(node_id, i * initial_value,
                                  j * initial_value, node_range))
            node_id += 1
    # Making a sink
    distances = []
    for node in (node_list):
        distances.append(distance(length_of_area / 2, breadth_of_area / 2,
                                  node.x, node.y))
        k=distances.index(min(distances))

    sink = BaseStation(0, node_list[k].x, node_list[k].y, node_range)
    node_list.append(sink)

    actual_node_list = []
    for node in node_list:
        ct = 1
        k = node_list.index(node)
        for j in node_list[k+1::]:
            # if node_list[i].x == node_list[j].x == node_list[i].y == node_list[j].y:
            if node.x == j.x and node.y == j.y:
                ct += 1
        if ct == 1:
            actual_node_list.append(node)

    node_id = 1
    for node in actual_node_list[:-1:]:
        node.id = node_id
        node_id += 1

    return actual_node_list


def high_lifetime_model(node_range, length_of_area, breadth_of_area):
    """Model that optimises lifetime."""
    node_list = []
    distances = []
    node_id = 1
    node_range = node_range - 2

    hex_along_l = calculate_p(breadth_of_area, node_range)
    hex_along_b = calculate_o(length_of_area, node_range)

    lattice = hexagonal_lattice_graph(hex_along_b, hex_along_l)
    x, y = generate_hex_mesh(lattice, node_range)
    centre_x, centre_y = generate_centers(x, y, node_range)
    for i in range(len(centre_x)):
        distances.append(distance(length_of_area / 2, breadth_of_area / 2,
                                  centre_x[i], centre_y[i]))

    k = distances.index(min(distances))
    inner_x, inner_y = draw_ring(centre_x[k], centre_y[k], node_range)
    for i in range(len(x)):
        node_list.append(Node(node_id, x[i], y[i], node_range))
        node_id += 1
    for i in range(len(inner_x)):
        node_list.append(Node(node_id, inner_x[i], inner_y[i], node_range))
        node_id += 1
    # for i in range(int(length_of_area/ node_range) + 1):
    #     node_list.append(Node(node_id, i*node_range - 1, breadth_of_area, node_range))
    #     node_id += 1
    node_list.append(BaseStation(0, centre_x[k], centre_y[k], node_range))


    popping_out = []
    for node in node_list[:-1:]:
        if node.x > length_of_area or node.x < 0 or node.y < 0 or node.y >breadth_of_area:
            popping_out.append(node)

    for node in popping_out:
        node_list.remove(node)

    actual_node_list = []
    for node in node_list:
        ct = 1
        k = node_list.index(node)
        for j in node_list[k+1::]:
            # if node_list[i].x == node_list[j].x == node_list[i].y == node_list[j].y:
            if node.x == j.x and node.y == j.y or distance_bw_nodes(node, j) <= 1:
                ct += 1
        if ct == 1:
            actual_node_list.append(node)

    node_id = 1
    for node in actual_node_list[:-1:]:
        node.id = node_id
        node_id += 1
    # print(len(actual_node_list), 'HEEHEHE')
    # print(len(node_list), 'LOLO')

    for node in actual_node_list:
        print(node.id, node.x, node.y)

    return actual_node_list


def high_reliability_model(node_range, length_of_area, breadth_of_area):
    """Model that preserves reliability"""
    node_list = []
    distances = []
    node_id = 1

    hex_along_l = calculate_p(length_of_area, node_range)
    hex_along_b = calculate_o(breadth_of_area, node_range)

    lattice = hexagonal_lattice_graph(hex_along_b, hex_along_l)
    x, y = generate_hex_mesh(lattice, node_range)
    centre_x, centre_y = generate_centers(x, y, node_range)
    for i in range(len(centre_x)):
        distances.append(distance(length_of_area / 2, breadth_of_area / 2,
                                         centre_x[i], centre_y[i]))

    k = distances.index(min(distances))
    for i in range(len(x)):
        node_list.append(Node(node_id, x[i], y[i], node_range))
        node_id += 1
    for i in range(len(centre_x)):
        node_list.append(Node(node_id, centre_x[i], centre_y[i], node_range))
        node_id += 1

    node_list.append(BaseStation(0, centre_x[k], centre_y[k], node_range))


    actual_node_list = []
    for node in node_list:
        ct = 1
        k = node_list.index(node)
        for j in node_list[k+1::]:
            # if node_list[i].x == node_list[j].x == node_list[i].y == node_list[j].y:
            if node.x == j.x and node.y == j.y:
                ct += 1
        if ct == 1:
            actual_node_list.append(node)

    node_id = 1
    for node in actual_node_list[:-1:]:
        node.id = node_id
        node_id += 1
    # print(len(actual_node_list), 'HEEHEHE')
    # print(len(node_list), 'LOLO')

    popping_out = []
    for node in actual_node_list[:-1:]:
        if node.x > breadth_of_area or node.x < 0 or node.y < 0 or node.y >length_of_area:
            popping_out.append(node)

    for node in popping_out:
        actual_node_list.remove(node)


    return actual_node_list


def sort_route(distance_dict, node_list):
    """Sort node.in_range of node according to increasing distance from sink.

    distance_dict has distances of each node from the sink.
    """
    for node in node_list:
        local_dict = {}
        in_range = node.in_range_nodes
        for mote in in_range:
            if mote in distance_dict:
                local_dict[mote] = distance_dict[mote]
        sorted_local_dict = sorted(local_dict.items(),
                                   key=operator.itemgetter(1))
        # gives a list containing a tuple of node with
        #  distance in increasing order
        node.routing_priority_nodes = sorted_local_dict

        sorted_by_ids = []
        for item in sorted_local_dict:
            item = list(item)
            item[0] = item[0].id
            sorted_by_ids.append(item)
        node.routing_priority_ids = sorted_by_ids


def transmit_packet(packet):
    """Transmit packet from node to the base station."""
    node = packet.from_node
    while node.in_base_range != 1:
        a = node.transmit(packet)
        node = node.routing_priority_nodes[0][0]
        if a == 0:
            break

    else:  # Checking if the node is in base range

        packet.route_id.append(0)


def get_sensors(csv):
    """Get all existing sensors from the csv."""
    return pd.read_csv(csv)


#def get_all_sensor_values(node_list):
#    """Get all sensor values."""
#    for node in node_list:
#        for sensor in node.sensors:
#            print(sensor.sensed_value)

def distance(x1,y1,x2,y2):
    """Find distance between x1,y1 and x2,y2"""
    return ((x2 - x1)**2 + (y2 - y1)**2)


def find_latency(packet_list):
    """Finds the latency of a packet_]ist.

    Give the absolute worst priority to each node in a packet.
     =>Add count_receiving_from of each node in the path and you get
     latency.
    """
    length_of_route = []
    max_length_packets = []
    worst_case_list = []

    for packet in packet_list:
        length_of_route.append(len(packet.route_id))
        # print(packet.route_id)
    print(length_of_route)# , "LEEEEEEEEEEEEEEEEEEEEE")

    maximum = max(length_of_route)
    # print(maximum)
    for i in range(len(length_of_route)):
        if length_of_route[i] == maximum:
            max_length_packets.append(packet_list[i])

    # print(max_length_packets)
    return maximum


def generate_packets(node_list):
    packet_list = []

    for i in range(len(node_list[:-1:])):
        if node_list[i].is_healthy == 1:
            packet_list.append(Packet(100, node_list[i].id, node_list[i],
                                       15, "MIL"))
    return packet_list


def mote_type(budget, model_type, length_of_area, breadth_of_area):
    """Decide which mote to use depending on budget."""
    if model_type == "low latency model":
        node_list1 = low_latency_model(90, length_of_area, breadth_of_area)
        node_list2 = low_latency_model(112, length_of_area, breadth_of_area)
        node_list3 = low_latency_model(135, length_of_area, breadth_of_area)

    elif model_type == "high lifetime model":
        node_list1 = high_lifetime_model(90, length_of_area, breadth_of_area)
        node_list2 = high_lifetime_model(112, length_of_area, breadth_of_area)
        node_list3 = high_lifetime_model(135, length_of_area, breadth_of_area)

    elif model_type == "high reliability model":
        node_list1 = high_reliability_model(90, length_of_area, breadth_of_area)
        node_list2 = high_reliability_model(112, length_of_area, breadth_of_area)
        node_list3 = high_reliability_model(135, length_of_area, breadth_of_area)

    checks = [False, False, False]
    if model_type is not None:
        if len(node_list3) * 7700 <= budget:
            node_type = ["Zolertia Z1", 135, 0.9504]  # Indoor range = 60
            checks[0] = True
        elif len(node_list2) * 6000 <= budget:
            node_type = ["Sky mote", 112, 0.6205]  # PER BIT Indoor range = 50
            checks[1] = True
        elif len(node_list1) * 800 <= budget:
            node_type = ["Arduino", 90, 0.275]  # Indoor range = 20 - 25
            checks[2] = True
        else:
            print("Not enough budget")
            sys.exit()

        if checks[0] is True:
            return ["Zolertia Z1", 135, 0.9504]
        elif checks[0] is False and checks[1] is True:
            return ["Sky mote", 112, 0.6205]
        else:
            return ["Arduino", 90, 0.275]
        return node_type

    else:
        return ["Zolertia Z1", 135, 0.9504]


def calculate_delay_1(x,node_props):
    if node_props[0]=="Zolertia Z1":
        delay=(len(x)-1)*2.049
    if node_props[0]=="Sky mote":
        delay=(len(x)-1)*2.054
    if node_props[0]=="Arduino":
        delay=(len(x)-1)*1
    return delay


def delete_node(node_index, network):
    node_list = network.node_list
    node_list[node_index].is_healthy = 0
    del node_list[node_index]
    for node in node_list:
        node.broadcast(node_list)
    distance_dict = distance_of_nodes(node_list)
    sort_route(distance_dict, node_list)
    network.node_list = node_list

    return node_list, network


def format_routing_priority(node_list):
    for node in node_list:
        for entry in node.routing_priority_nodes:
            if entry[0] == node:
                k = node.routing_priority_nodes.index(entry)
                del node.routing_priority_nodes[k]
                del node.routing_priority_ids[k]
        for nodu in node.in_range_nodes:
            if nodu == node:
                j = node.in_range_nodes.index(nodu)
                del node.in_range_nodes[j]
                del node.in_range_ids[j]
    return node_list

def calculate_battery(packet_list, node_list, network):
    below_10_percent = []
    for packet in packet_list:
        for node in packet.route_node:
            # Replace 2 with Akshobya value(put as parameter in node)
            node.battery -= network.node_properties[2] + random.randint(0, int(0.05 * network.node_properties[2]))
    for node in node_list:
        if node.battery <= 10:
            # print(node.id, node.battery)
            below_10_percent.append(node)
    for node in below_10_percent:
        node.is_healthy = 0
        node_list, network = delete_node(node_list.index(node), network)
    # print("LOL2")

    return node_list, network

def calculate_lifetime(node_list, in_sink_range, network):
    count = 0
    to_graph_dict = {}
    for node in node_list[:-1:]:
        to_graph_dict[node.id] = [100]
    while in_sink_range != []:
        count += 1
    # while count <=2:
        for node in node_list[:-1:]:
            # print([(node.id, node.battery) for node in node_list], "KYU")
            # print()
            if node.is_healthy == 1:
                packet = Packet(100, node.id, node, 15, "MIL")
                transmit_packet(packet)
                # print(packet.route_id)
                # print()
                node_list, network = calculate_battery([packet], node_list, network)
                in_sink_range = node_list[-1].broadcast(node_list[-2::-1])
                if in_sink_range == []:
                    break
                # print([(node.id, node.battery) for node in node_list], "KYA")
                # print()
        for mote in node_list[:-1:]:
            to_graph_dict[mote.id].append(mote.battery)

        # print(len(node_list))
        in_sink_range = node_list[-1].broadcast(node_list[-2::-1])
        # print([mote.id for mote in in_sink_range], "in_sink_range")


    return count, to_graph_dict

def farthest_node(node_list):
    distance_dict = distance_of_nodes(node_list)
    node = 0
    dist = 0
    for mote in distance_dict:
        if distance_dict[mote] > dist:
            dist = distance_dict[mote]
            node = mote
    return node

def deepesh_latency(node_list, network):
    backup_node_list = node_list
    far_node = farthest_node(node_list)
    far_node_packet = Packet(100, far_node.id, far_node, 15, "MIL")
    transmit_packet(far_node_packet)
    for node in far_node_packet.route_node[1:-1]:
        node_list = backup_node_list
        for mote in backup_node_list:
            print(mote.id, end = " ")
        print("ini")
        node_list, network = delete_node(node.id - 1, network)
        for mote in node_list:
            print(mote.id, end = " ")
        print("fina")
        k = find_latency(generate_packets(node_list))
        print(k,"DEEEEEEEEEEEEEEEEPESH")



def start():
    """Start the simulator."""
    budget = 21600000000
    length = 800
    breadth = 400

    # model_type = None
    model_type = "high lifetime model"
    # model_type = "low latency model"
    # model_type = "high reliability model"

    node_id = [1, 2, 3, 4]
    x = [200, 100, 150, 200]  # x coordinate of the nodes
    y = [200, 50, 150, 100]  # y coordinate of the nodes
    packet_list = []  # List containing all the packets active in the network

    # Making a list that contains all the nodeslen(packet.route_node))
    node_props = mote_type(budget, model_type, length, breadth)

    network = Network(length, breadth, model=model_type,
                      node_properties=node_props)

    # network = Network(length, breadth, node_properties=node_props,node_id=node_id, x=x, y=y)

    node_list = network.define()

    node_list = network.initialize()
    for node in node_list:
        node.broadcast(node_list)

    distance_dict = distance_of_nodes(node_list)
    sort_route(distance_dict, node_list)

    print()

    packet_list = generate_packets(node_list)
    for packet in packet_list:
        transmit_packet(packet)

    print(find_latency(packet_list))

    draw_figure(length, breadth, node_list, True)

    relative_lifetime, to_graph = calculate_lifetime(node_list, network.in_sink_range, network)

    print("Relative lifetime:", relative_lifetime)
    for node in to_graph:
        if node == 12:
            while len(to_graph[node]) < relative_lifetime:
                to_graph[node].append(0)
            plt.plot(to_graph[node], label=str(node))
            plt.legend(loc='lower left')
        plt.xlabel("Number of iterations")
        plt.ylabel("Battery values")
        plt.title("Lifetime of each node")

    draw_figure(length, breadth, node_list, True)

    plt.show()
