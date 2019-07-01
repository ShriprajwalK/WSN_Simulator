# TODO: Make base_station part of node_list so that the program length becomes smaller.
# => Easy/painful? deals with basic python

# TODO: Refactor the code into different files.
# => Easy/painful? gotta look into this after everything is done

# TODO: Implement draw packets
# => Idk.

# TODO: Implement battry life and time taken.
# => Medium? Deals with threading. Not sure how to go about all this.

# TODO: Implement hexagonal model(reliable)
# => Hard? Need a general formulae for coordinates

# TODO: Implement high lifetime model
# => Same as hexagonal.




import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import operator

plt.close() # To close any other plt windows just in case

class Node(object):
    """Each Node belongs to this class.
    General properties of a node are defined here."""

    def __init__(self,id,x,y,range,battery=100,rank=1):
        # Inititialising/Defining the node

        self.id = id
        self.x = x
        self.y = y
        self.range = range
        self.battery = battery

        self.in_range_ids = []
        self.in_range_nodes = []

        self.in_base_range = 0

        self.routing_priority_nodes = []
        self.routing_priority_ids = []

        self.transmitting_to = 0
        self.receiving_from = []
        self.count_receiving_from = 0

        self.memory = ""


    def broadcast(self, node_list):
        # Make-do function that finds all other nodes that are in range.
        # A function because nodes can die. Running this function will find out what other nodes are in range of each node.
        """node_list = List of nodes that are part of the network
        Possible improvements: Instead of O(n^2), do something more efficient"""

        for node in node_list:
            if distance(self,node) <= (self.range)**2 : # Checking distances of each node
                self.in_range_ids.append(node.id)
                self.in_range_nodes.append(node)
        return self.in_range_nodes


    def transmit(self,packet):
        # node.transmit(packet) transmits a packet to the node with the highest priority.
        if self.in_base_range == 1:
            packet.route.append(0)
            return 0
        else:
            node_to = self.routing_priority_nodes[0][0]
            if self not in node_to.receiving_from: # Helps in battery consumption. A node receiving from more stuff dies faster.
                node_to.receiving_from.append(self)
                node_to.count_receiving_from +=1

            packet.route_id.append(node_to.id)
            packet.route_node.append(node_to)
            node_to.receive()
            return node_to

    def receive(self):
        pass

    def remove_path(from_node, to_node):
        to_node.count_receiving_from -= 1
        from_node.transmitting_to = 0


class BaseStation(Node):
    """Only one base station exists in a wireless sensor network
        Has the same properties as a node.
    """

    def __init__(self,id,x,y,range):
        # Defining the base station
        Node.__init__(self,id,x,y,range)
        self.id = id
        self.x = x
        self.y = y
        self.range = range


class Packet(object):
    """Packet and it's properties are given here."""
    def __init__(self, from_node_id,from_node, size, message):
        # Defining a packet
        self.from_node_id = from_node_id
        self.from_node = from_node
        self.size = size
        self.message = message
        self.route_id = []
        self.route_node = []


    def packet_loss(self):
        # Possible property of a packet
        pass


def distance(node1, node2):
    # Finds the distance between node1 and node2
    return (node1.x - node2.x)**2 + (node1.y - node2.y)**2

def distance_of_nodes(sink, node_list):
    """Returns a dict containing distance b/w nodes and sink nodes"""

    distance_dict = {}
    for node in node_list:
        distance_dict[node] = distance(sink,node)
    return distance_dict

def define_network(length_of_area, breadth_of_area, node_range, model = None, id = None, x = None, y = None):
    # init network. Defining the network and stuff

    node_list = []

    if model == None:
        number_of_nodes = len(id)
        for i in range(number_of_nodes):
            node_list.append(Node(id[i],x[i],y[i],node_range)) # Appending the nodes to the list

    if model == "low_latency_model":
        node_list = low_latency_model(node_range, length_of_area, breadth_of_area)

    return node_list

def initialize_network(node_list):
    """Start your network and stuff"""
    for node in node_list:
        node.broadcast(node_list)
    in_sink_range = sink.broadcast(node_list)
    for node in in_sink_range:
        node.in_range_ids.append(0)
        node.in_base_range = 1

def draw_packets(packet_list):
    x = np.linspace(0,45,1000)
    for packet in packet_list:
        for i in range(len(packet.route_node)):
            if i < (len(packet.route_node)-1):
                # to_node = route_node[i+1]
                # from_node = route_node[i]
                # plt.plot(x,(packet.to_node.y - packet.from_node.y)/(packet.to_node.x - packet.from_node.x)*x, '--c')
                # plt.xlim(to_node.x, from_node.x)
                # plt.ylim(to_node.y, from_node.y)
                plt.plot(x, x + 1, '--c')
    plt.show()


def draw_figure(length,breadth,node_list,base_station = None):
    # Draws the whole network.

    fig = plt.figure() # plt stuff that seem to be a must to draw circles.
    ax = fig.add_subplot(1,1,1)

    plt.scatter(base_station.x,base_station.y) # Plotting the base station
    base_range = plt.Circle((base_station.x, base_station.y),base_station.range,fill=False,color = "b") # Base station radius

    for node in node_list:
        plt.scatter(node.x,node.y) # Plotting the nodes

        plt.plot([0,length,length,0,0],[0,0,breadth,breadth,0])
        node_range = plt.Circle((node.x,node.y),node.range,fill=False) #Plotting the circle for each node
        plt.gca().set_aspect('equal') # making x-axis and y-axis equal
        # Trying to display id numbers on the nodes:
        ax.annotate(node.id, (node.x, node.y)) #Displaying node ids along with the nodes on the graph
        ax.add_patch(node_range) # Finally drawing the circle.

    ax.annotate("sink node", (base_station.x, base_station.y))
    ax.add_patch(base_range) # Adding the circle base_range to the figure
    plt.title("Simulator plot")
    plt.xlabel("Breadth of given area")
    plt.ylabel("Length of given area")

    plt.show()

def low_latency_model(node_range, length_of_area, breadth_of_area):
    # Model that Anish came up with for relatively low latency
    # at a moderate cost.

    node_list = []
    id = 1


    initial_value = node_range/np.sqrt(2)
    num_nodes_along_length = int(length_of_area/initial_value)
    num_nodes_along_breadth = int(breadth_of_area/initial_value)

    for i in range(num_nodes_along_length+1):
        for j in range(num_nodes_along_breadth+1):
            node_list.append(Node(id, i*initial_value, j*initial_value, node_range))
            id += 1
    print("Number of nodes required for a reasonable latency is",len(node_list))
    return node_list

def sort_route(distance_dict,node_list):
    # Sorting node.in_range of each node according to neighbours nearest to the sink
    # distance_dict has distances of each node from the sink.
    for node in node_list:
        local_dict = {}
        in_range = node.in_range_nodes
        for mote in in_range:
            if mote in distance_dict:
                local_dict[mote] = distance_dict[mote]
        sorted_local_dict = sorted(local_dict.items(), key=operator.itemgetter(1)) # gives a list containing a tuple of node with distance in increasing order
        node.routing_priority_nodes = sorted_local_dict

        sorted_by_ids = []
        for item in sorted_local_dict:
            item = list(item)
            item[0] = item[0].id
            sorted_by_ids.append(item)
        node.routing_priority_ids = sorted_by_ids

def transmit_packet(node,packet):
    while node.in_base_range != 1:
        node.transmit(packet)
        node = node.routing_priority_nodes[0][0]

    else:
        packet.route_id.append(0)

length_of_area = 100
breadth_of_area = 100

id = [1,2,3,4]
x = [20,10,15,20] # x coordinate of the nodes
y = [20,5,15,10] # y coordinate of the nodes
node_range = 27 # Range of the nodes
packet_list = [] #List containing all the packets active in the network


# Making a list that contains all the nodeslen(packet.route_node))
node_list = define_network(length_of_area, breadth_of_area, node_range,model = "low_latency_model")

sink = BaseStation(0,length_of_area/3 , breadth_of_area/3,node_range) # Making a sink
## The sink is not in node_list.It makes node_list type as None for some reason.

initialize_network(node_list)

distance_dict = distance_of_nodes(sink,node_list)
sort_route(distance_dict,node_list)

for i in range(len(node_list)):
    packet_list.append(Packet(i+1,node_list[i],15,"Shreyashoe"))
for packet in packet_list:
    transmit_packet(packet.from_node,packet)

for packet in packet_list:
    print(packet.from_node.id, packet.route_id)
# Plot at the end
draw_figure(length_of_area, breadth_of_area, node_list,sink)
