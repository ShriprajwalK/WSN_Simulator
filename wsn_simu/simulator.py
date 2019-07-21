"""A Wireless Sensor Network Simulator to simulate Wireless Sensor Networks."""

# TODO: Refactor the code into different files.
# => Easy/painful? gotta look into this after everything is done

# TODO: Implement draw packets
# => Idk.

# TODO: Implement battry life and time taken.
# => Medium? Deals with threading? Not sure how to go about all this.

# TODO: Implement hexagonal model(reliable) and lifetime model
# => Hard? Need a general formulae for coordinates
import pandas as pd
import sys
# sys.path.append('C:\\Users\Anish\Desktop\MLab\MADHOC\Sim_TBD')

from wsn_simu.node.node import Node, BaseStation, distance_bw_nodes
from wsn_simu.node.hexagonal_model import calculate_o, calculate_p
from wsn_simu.node.hexagonal_model import generate_hex_mesh, draw_ring
from wsn_simu.node.hexagonal_model import hexagonal_lattice_graph
from wsn_simu.node.hexagonal_model import generate_centers
from wsn_simu.packet.packet import Packet
from wsn_simu.sensors.sensors import Sensor

import logging



logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import operator
    # import time
    import sys

except Exception:
    print("Dependencies not installed")
    logging.error("Dependencies not installed")


plt.close()  # To close any other plt windows just in case


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Network(object):
    """Simulate the network using everything else in the code.

    Network definition, initialising and lifetime etcetra are calculated.
    """

    def __init__(self, length_of_area, breadth_of_area, model=None,
                 node_properties=None, node_id=None, x=None, y=None):
        """Init Network. Defining the network and stuff."""
        self.length_of_area = length_of_area
        self.breadth_of_area = breadth_of_area
        self.model = model
        self.node_properties = node_properties
        self.node_id = node_id
        self.x = x
        self.y = y

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
            node.in_range_ids.append(0)
            node.in_base_range = 1

        return self.node_list

    def is_alive(self):
        """Check if the network is alive."""
        alive = False
        for node in self.node_list:
            if node.in_base_range == 1:
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
    initial_value = node_range / np.sqrt(2)
    num_nodes_along_length = int(length_of_area / initial_value)
    num_nodes_along_breadth = int(breadth_of_area / initial_value)

    for i in range(num_nodes_along_length + 1):
        for j in range(num_nodes_along_breadth + 1):
            node_list.append(Node(node_id, i * initial_value,
                                  j * initial_value, node_range))
            node_id += 1
    # Making a sink
    sink = BaseStation(0, length_of_area / 2, breadth_of_area / 2, node_range)
    node_list.append(sink)
    return node_list


def high_lifetime_model(node_range, length_of_area, breadth_of_area):
    """Model that optimises lifetime."""
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
    inner_x, inner_y = draw_ring(centre_x[k], centre_y[k], node_range)
    for i in range(len(x)):
        node_list.append(Node(node_id, x[i], y[i], node_range))
        node_id += 1
    for i in range(len(inner_x)):
        node_list.append(Node(node_id, inner_x[i], inner_y[i], node_range))
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

    # print(len(actual_node_list), 'HEEHEHE')
    # print(len(node_list), 'LOLO')

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
    return node_list

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
        node.transmit(packet)
        node = node.routing_priority_nodes[0][0]

    else:  # Checking if the node is in base range

        packet.route_id.append(0)



def get_sensors(csv):
    """Get all existing sensors from the csv."""
    return pd.read_csv(csv)


def get_all_sensor_values(node_list):
    """Get all sensor values."""
    for node in node_list:
        for sensor in node.sensors:
            print(sensor.sensed_value)

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
        print(packet.route_id)
    print(length_of_route, "LEEEEEEEEEEEEEEEEEEEEE")

    # maximum = max(length_of_route)
    # print(maximum)
    # for i in range(len(length_of_route)):
    #     if length_of_route[i] == maximum:
    #         max_length_packets.append(packet_list[i])

    for packet in packet_list:
        worst_case = 0
        print(packet.route_id)
        for node in packet.route_node[1::]:
            worst_case += node.count_receiving_from + 1
            # + 1 cuz a node can transmit it's message before transmitting
            # it's neighbours message.
            print(worst_case,)
        worst_case_list.append(worst_case)
        print((worst_case, "NYAN"))
    print(max(worst_case_list))
    # return maximum


def mote_type(budget, model_type, length_of_area, breadth_of_area):
    """Decide which mote to use depending on budget."""
    if model_type == "low latency model":
        node_list1 = low_latency_model(100, length_of_area, breadth_of_area)
        node_list2 = low_latency_model(125, length_of_area, breadth_of_area)
        node_list3 = low_latency_model(150, length_of_area, breadth_of_area)

    elif model_type == "high lifetime model":
        node_list1 = high_lifetime_model(100, length_of_area, breadth_of_area)
        node_list2 = high_lifetime_model(125, length_of_area, breadth_of_area)
        node_list3 = high_lifetime_model(150, length_of_area, breadth_of_area)

    elif model_type == "high reliability model":
        node_list1 = high_reliability_model(100, length_of_area, breadth_of_area)
        node_list2 = high_reliability_model(125, length_of_area, breadth_of_area)
        node_list3 = high_reliability_model(150, length_of_area, breadth_of_area)

    checks = [False, False, False]

    if len(node_list3) * 7700 <= budget:
        node_type = ["Zolertia Z1", 150]  # Indoor range = 60
        checks[0] = True
    elif len(node_list2) * 6000 <= budget:
        node_type = ["Sky mote", 125]  # Indoor range = 50
        checks[1] = True
    elif len(node_list1) * 800 <= budget:
        node_type = ["Arduino", 100]  # Indoor range = 20-25
        checks[2] = True
    else:
        print("Not enough budget")
        sys.exit()

    if checks[0] is True:
        return ["Zolertia Z1", 150]
    elif checks[0] is False and checks[1] is True:
        return ["Sky mote", 125]
    else:
        return ["Arduino", 100]

    return node_type


def calculate_delay_1(x,node_props):
    if node_props[0]=="Zolertia Z1":
        delay=(len(x)-1)*2.049
    if node_props[0]=="Sky mote":
        delay=(len(x)-1)*2.054
    if node_props[0]=="Arduino":
        delay=(len(x)-1)*1
    return delay



def start():
    """Start the simulator."""
    budget = 21600000000
    length = 800
    breadth = 800
    model_type = "high lifetime model"

    # node_id = [1, 2, 3, 4]
    # x = [20, 10, 15, 20]  # x coordinate of the nodes
    # y = [20, 5, 15, 10]  # y coordinate of the nodes
    packet_list = []  # List containing all the packets active in the network

    # Making a list that contains all the nodeslen(packet.route_node))
    node_props = mote_type(budget, model_type, length, breadth)

    network = Network(length, breadth, model=model_type,
                      node_properties=node_props)

    node_list = network.define()
    # print(node_list)

    node_list = network.initialize()
    for node in node_list:
        node.broadcast(node_list)
    # for node in node_list:
    #     if node.is_healthy == 1:
    #         print(node.id)
    distance_dict = distance_of_nodes(node_list)
    sort_route(distance_dict, node_list)

    ct = 1
    for i in range(len(node_list)):
        if node_list[i].is_healthy == 1:
            packet_list.append(Packet(100, node_list[i].id, node_list[i],
                                       15, "MIL"))
            ct += 1
    print(ct)

    test_packet = Packet(100, 5, node_list[4], 15, "Sensor value")
    for test_packet in packet_list:
        transmit_packet(test_packet)
        print(test_packet.route_id, "HAHAHA")
    #    delay=calculate_delay_1(test_packet.route_id,node_props)
    #    print(delay)
    #sensor_list = get_sensors("wsn_simu/Sensor Data.csv")
    #sensor_list = sensor_list.set_index("Name", drop=False)
    #sensor = Sensor("DHT 11_T", "Temperature", sensor_list)
    #print(sensor.sense_value())
    # # print(node_list[4].in_range_ids)
    #
    # # Plot at the end
    #for node in node_list:
    #    if distance(node_list[-1].x, node_list[-1].y, node.x, node.y) <= node_list[-1].range:
    #        print(node.id)
    #for node in network.in_sink_range:
    #    print(node.id, end=' ')

    find_latency(packet_list)

    draw_figure(length, breadth, node_list, True)

    #print(generate_hex_mesh(hexagonal_lattice_graph(12,14), 1))
    plt.show()
