import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.close()

class Node(object):
    """Each Node belongs to this class.
    General properties of a node are defined here."""

    def __init__(self,id,x,y,range,battery=100,rank=1):
        # Inititialising/Defining the node
        self.x = x
        self.y = y
        self.range = range
        self.battery = battery
        self.in_range = []

    def broadcast(self, node_list):
        # Finds all other nodes that are in range.
        # A function because nodes can die. Running this function will find out what other nodes are in range of each node.
        """node_list = List of nodes that are part of the network"""
        for node in node_list:
            if np.abs(node.x - self.x) < self.range and np.abs(node.x - self.x) < self.range : # Checking distances of each node
                self.in_range.append(node)

class Base_Station(Node):
    """Only one base station exists in a wireless sensor network
        Has the same properties as a node."""
    def __init__(self):
        pass



def initialize_network(length_of_area, breadth_of_area, node_range, model=None, id = None, x=None, y=None):
    # init network. Assigning nodes and stuff
    node_list = []

    if model == None:
        number_of_nodes = len(id)

        for i in range(number_of_nodes):
            node_list.append(Node(id[i],x[i],y[i],node_range)) # Appending the nodes to the list

    if model == "low_latency_model":
        node_list = low_latency_model(node_range, length_of_area, breadth_of_area)

    return node_list


def draw_nodes(node_list):
    for node in node_list:
        plt.scatter(node.x,node.y) # Plotting the nodes
        node_range = plt.Circle((node.x,node.y),node.range,fill=False) #Plotting the circle
        plt.gca().set_aspect('equal') # making x-axis and y-axis equal
        ax.add_patch(node_range)
        node.broadcast(node_list)
    plt.show()

def draw_area(length, breadth):
    plt.plot([0,length,length,0,0],[0,0,breadth,breadth,0])

def low_latency_model(node_range, length_of_area, breadth_of_area):
    node_list = []
    id = 0

    # initial_value = np.sqrt(2)*node_range
    num_nodes_along_length = int(length_of_area/node_range)
    num_nodes_along_breadth = int(breadth_of_area/node_range)

    #node_list.append(Node(id, initial_value, initial_value, node_range))

    id += 1

    for i in range(1,num_nodes_along_length):
        for j in range(1,num_nodes_along_breadth):
            node_list.append(Node(id, i*node_range,j*node_range, node_range))
            id += 1
    print("Number of nodes required for a reasonable latency is",len(node_list))
    return node_list


length_of_area = 50
breadth_of_area = 50

id = [1,2,3,4]
x = [20,10,15,20] # x coordinates of the node
y = [20,5,15,10] # y coordinates of the node
node_range = 10 # Range of the motes

fig=plt.figure()
ax=fig.add_subplot(1,1,1)

draw_area(length_of_area, breadth_of_area)

node_list= initialize_network(length_of_area, breadth_of_area, node_range,model = "low_latency_model") # List containing the nodes
draw_nodes(node_list)

print(node_list[0].x)
