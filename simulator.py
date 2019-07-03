"""A Wireless Sensor Network Simulator to simulate Wireless Sensor Networks."""

# TODO: Refactor the code into different files.
# => Easy/painful? gotta look into this after everything is done

# TODO: Implement draw packets
# => Idk.

# TODO: Implement battry life and time taken.
# => Medium? Deals with threading? Not sure how to go about all this.

# TODO: Implement hexagonal model(reliable) and lifetime model
# => Hard? Need a general formulae for coordinates
import logging

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

try:
    import matplotlib.pyplot as plt
    # import matplotlib.patches as mpatches
    import numpy as np
    import operator
    # import time
    import random

except Exception:
    print("Dependencies not installed")
    logging.error("Dependencies not installed")


plt.close()  # To close any other plt windows just in case


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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

        self.in_range_ids = []
        self.in_range_nodes = []

        self.in_base_range = 0
        self.is_healthy = 1

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
        for node in node_list:
            if distance(self, node) <= (self.range)**2:
                # Checking distances of each node
                if node.is_healthy == 1 and node not in self.in_range_nodes:
                    self.in_range_ids.append(node.id)
                    self.in_range_nodes.append(node)
        return self.in_range_nodes

    def battery_consumed_for_packet(self, packet):
        """Use properties of the packet like size etc.to affect the battery."""
        initial_value = self.battery
        dist = distance(self, self.routing_priority_nodes[0][0])
        self.battery -= 0.001 * packet.message_size * dist
        logging.info("%d battery %d", self.id, self.battery)
        return initial_value - self.battery

    def transmit(self, packet):
        """Transmit a packet to the next node with highest priority."""
        # node.transmit(packet) transmits a packet to
        # the node with the highest priority.
        self.battery_consumed_for_packet(packet)
        if self.is_healthy == 1:
            if packet.type == 100:
                if self.in_base_range == 1:
                    packet.route_id.append(0)
                    return 0
                else:
                    node_to = self.routing_priority_nodes[0][0]
                    if self not in node_to.receiving_from:
                        """ Helps in battery consumption.
                        A node receiving from more stuff dies faster."""
                        node_to.receiving_from.append(self)
                        node_to.count_receiving_from += 1

                    node_to.receive(packet)
                    packet.route_id.append(node_to.id)
                    packet.route_node.append(node_to)
                    return node_to
            elif packet.type == 101:
                # packet.route_id.append(self.id)
                # packet.route_node.append(self)
                packet.destination.receive(packet)

        else:
            return 0

    def receive(self, packet):
        """Receive a packet from another node."""
        if packet.type == 101:
            print(packet.route_id)
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


class Packet(object):
    """Packet and it's properties are given here."""

    def __init__(self, node_type, from_node_id, from_node, message_size,
                 message, destination="sink"):
        # Defining a packet
        """
        Packet type: To differentiate between info and acks.

                    = 100 for info
                    = 101 for acks
        """
        self.type = node_type
        self.from_node_id = from_node_id
        self.from_node = from_node
        self.message_size = message_size
        self.message = message
        self.route_id = [from_node_id]
        self.route_node = [from_node]
        self.destination = destination

    def packet_loss(self):
        """Possible property of a packet."""
        pass


class Sensor(object):
    """
    Class for different types of sensors.

    Different kinds
    """

    def __int__(self, name=None):
        """Inititialise sensor values."""
        self.name = name
        if self.name in ["Temperature", "Humidity", "DHT11", "DHT22"]:
            self.sensed_value = {"temp": random.randint(0, 50),
                                 "humidity": random.randint(20, 90)}
            logging.info("""temp value is measured in Celsius and humidity is
                            measured in percentage""")
            return self.sensed_value
        if self.name == "Pressure" or self.name == "Barometric":
            # returns pressure in hPa
            self.sensed_value = {"pressure": random.randint(300, 1100)}
            logging.info("pressure value is measured in hPa")
            return self.sensed_value
        if self.name == "":
            pass


class Obstacle(object):
    """Class for obstacles.

    There can be obstacles that reduce node range
    """

    def __init__(self, obstacle_property):
        """Inititialise properties."""
        self.property = obstacle_property


def distance(node1, node2):
    """Find the distance between node1 and node2."""
    return (node1.x - node2.x)**2 + (node1.y - node2.y)**2


def distance_of_nodes(node_list):
    """Return a dict containing distance b/w nodes and sink nodes."""
    distance_dict = {}
    for node in node_list:
        distance_dict[node] = distance(node_list[-1], node)
    return distance_dict


def define_network(length_of_area, breadth_of_area,
                   node_range, model=None, node_id=None, x=None, y=None):
    """Init network. Defining the network and stuff."""
    node_list = []

    if model is None:
        number_of_nodes = len(node_id)
        for i in range(number_of_nodes):
            node_list.append(Node(id[i], x[i], y[i], node_range))
            # Appending the nodes to the list

    if model == "low_latency_model":
        node_list = low_latency_model(node_range, length_of_area,
                                      breadth_of_area)

    return node_list


def initialize_network(node_list):
    """Start your network and stuff."""
    for node in node_list:
        node.broadcast(node_list)
    in_sink_range = node_list[-1].broadcast(node_list[-2::-1])
    for node in in_sink_range:
        node.in_range_ids.append(0)
        node.in_base_range = 1


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


def draw_figure(length, breadth, node_list):
    """Draw the whole network."""
    fig = plt.figure()  # plt stuff that seem to be a must to draw circles.
    ax = fig.add_subplot(1, 1, 1)

    plt.scatter(node_list[-1].x, node_list[-1].y)  # Plotting the base station
    base_range = plt.Circle((node_list[-1].x, node_list[-1].y),
                            node_list[-1].range, fill=False, color="b")
    # Base station radius

    for node in node_list[:-1:]:
        plt.scatter(node.x, node.y)  # Plotting the nodes

        plt.plot([0, length, length, 0, 0], [0, 0, breadth, breadth, 0])
        node_range = plt.Circle((node.x, node.y), node.range, fill=False)
        # Plotting the circle for each node
        plt.gca().set_aspect('equal')  # making x-axis and y-axis equal
        # Trying to display id numbers on the nodes:
        ax.annotate(node.id, (node.x, node.y))
        # Displaying node ids along with the nodes on the graph
        ax.add_patch(node_range)  # Finally drawing the circle.

    ax.annotate("sink node", (node_list[-1].x, node_list[-1].y))
    ax.add_patch(base_range)  # Adding the circle base_range to the figure
    plt.title("Simulator plot")
    plt.xlabel("Breadth of given area")
    plt.ylabel("Length of given area")

    plt.show()


def low_latency_model(node_range, length_of_area, breadth_of_area):
    """Model that Anish came up with for relatively low latency.

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
    print("Num of nodes required for reasonable latency is", len(node_list))
    return node_list


def sort_route(distance_dict, node_list):
    """Sort node.in_range of node_list according to increasing distance from sink.

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


def transmit_packet(node, packet):
    """Transmit packet from node to the base station."""
    while node.in_base_range != 1:
        node.transmit(packet)
        node = node.routing_priority_nodes[0][0]

    else:  # Checking if the node is in base range
        packet.route_id.append(0)


def get_all_sensor_values(node_list):
    """Get all sensor values."""
    for node in node_list:
        for sensor in node.sensors:
            print(sensor.sensed_value)


length_of_area = 100
breadth_of_area = 100

node_id = [1, 2, 3, 4]
x = [20, 10, 15, 20]  # x coordinate of the nodes
y = [20, 5, 15, 10]  # y coordinate of the nodes
node_range = 27  # Range of the nodes
packet_list = []  # List containing all the packets active in the network

# Making a list that contains all the nodeslen(packet.route_node))
node_list = define_network(length_of_area, breadth_of_area, node_range,
                           model="low_latency_model")
# Making a sink
sink = BaseStation(0, length_of_area / 3, breadth_of_area / 3, node_range)

node_list.append(sink)

initialize_network(node_list)

distance_dict = distance_of_nodes(node_list)
sort_route(distance_dict, node_list)

for i in range(len(node_list)):
    packet_list.append(Packet(100, i + 1, node_list[i], 15, "Shreyashoe"))

test_packet = Packet(100, 36, node_list[35], 15, "Sensor value")
transmit_packet(test_packet.from_node, test_packet)
print(test_packet.route_id)
# Plot at the end
draw_figure(length_of_area, breadth_of_area, node_list)
