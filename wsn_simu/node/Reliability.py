"""Plotting the Reliability model."""

import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt
from networkx.generators.classic import empty_graph
from networkx.classes import set_node_attributes


def hexagonal_lattice_graph(m, n, periodic=False, with_positions=True,
                            create_using=None):
    """Return an `m` by `n` hexagonal lattice graph.

    The *hexagonal lattice graph* is a graph whose nodes and edges are
    the `hexagonal tiling`_ of the plane.

    The returned graph will have `m` rows and `n` columns of hexagons.
    `Odd numbered columns`_ are shifted up relative to even numbered columns.

    Positions of nodes are computed by default or `with_positions is True`.
    Node positions creating the standard embedding in the plane
    with sidelength 1 and are stored in the node attribute 'pos'.
    `pos = nx.get_node_attributes(G, 'pos')` creates a dict ready for drawing.

    .. _hexagonal tiling: https://en.wikipedia.org/wiki/Hexagonal_tiling
    .. _Odd numbered columns:
     http://www-cs-students.stanford.edu/~amitp/game-programming/grids/

    Parameters
    ----------
    m : int
        The number of rows of hexagons in the lattice.

    n : int
        The number of columns of hexagons in the lattice.

    periodic : bool
        Whether to make a periodic grid by joining the boundary vertices.
        For this to work `n` must be odd and both `n > 1` and `m > 1`.
        The periodic connections create another row and column of hexagons
        so these graphs have fewer nodes as boundary nodes are identified.

    with_positions : bool (default: True)
        Store the coordinates of each node in the graph node attribute 'pos'.
        The coordinates provide a lattice with vertical columns of hexagons
        offset to interleave and cover the plane.
        Periodic positions shift the nodes vertically in a nonlinear way so
        the edges don't overlap so much.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
        If graph is directed, edges will point up or right.

    Returns
    -------
    NetworkX graph
        The *m* by *n* hexagonal lattice graph.

    """
    G = empty_graph(0, create_using)
    if m == 0 or n == 0:
        return G
    if periodic and (n % 2 == 1 or m < 2 or n < 2):
        msg = "periodic hexagonal lattice needs m > 1, n > 1 and even n"
        raise NetworkXError(msg)

    M = 2 * m    # twice as many nodes as hexagons vertically
    rows = range(M + 2)
    cols = range(n + 1)
    # make lattice
    col_edges = (((i, j), (i, j + 1)) for i in cols for j in rows[:M + 1])
    row_edges = (((i, j), (i + 1, j)) for i in cols[:n] for j in rows
                 if i % 2 == j % 2)
    G.add_edges_from(col_edges)
    G.add_edges_from(row_edges)
    # Remove corner nodes with one edge
    G.remove_node((0, M + 1))
    G.remove_node((n, (M + 1) * (n % 2)))

    # identify boundary nodes if periodic
    if periodic:
        for i in cols[:n]:
            G = contracted_nodes(G, (i, 0), (i, M))
        for i in cols[1:]:
            G = contracted_nodes(G, (i, 1), (i, M + 1))
        for j in rows[1:M]:
            G = contracted_nodes(G, (0, j), (n, j))
        G.remove_node((n, M))

    # calc position in embedded space
    ii = (i for i in cols for j in rows)
    jj = (j for i in cols for j in rows)
    xx = (0.5 + i + i // 2 + (j % 2) * ((i % 2) - .5)
          for i in cols for j in rows)
    h = sqrt(3) / 2
    if periodic:
        yy = (h * j + .01 * i * i for i in cols for j in rows)
    else:
        yy = (h * j for i in cols for j in rows)
    # exclude nodes not in G
    pos = {(i, j): (x, y) for i, j, x, y in zip(ii, jj, xx, yy) if (i, j) in G}
    set_node_attributes(G, pos, 'pos')
    return G


def calculate_o(b, r):
    """Calculate the number of horizontal hexagons."""
    o = (b / (r * sqrt(3))) // 1
    return o


def calculate_p(l, r):
    """Calculate the number of vertical hexagons."""
    p = (l / (2 * r)) // 1
    return p


def generate_hex_mesh(G):
    """Generate The Hex Mesh Co-ordinates"""
    x=[]
    y=[]
    d = nx.get_node_attributes(G, 'pos')
    var = (list(d.values()))

    for i in range(len(var)):
        x.append(r * var[i][1])

    for i in range(len(var)):
        y.append(r * var[i][0])

    return x,y


def generate_centers(x, y):
    """Generate Centers of the Hexagons"""
    x1=[]
    y1=[]
    y2=[]

    for i in range(len(x)):
        if y[i] % (3 * r / 2)==0:
            x1.append(x[i])
            y1.append(y[i])
    y2=y1

    for i in range(len(y1)):
            y2[i]=(y1[i] + r)
    y1=y2

    return x1,y1


def distance(s1,s2,x,y):
    """Find the distance between node1 and node2."""
    return (s1 - x)**2 + (s2 - y)**2


def find_sink(b,l,x1,y1,r):
    s1=b/2
    s2=l/2
    dist1=20*r
    for i in range(len(x1)):    
        dist=distance(s1,s2,x1[i],y1[i])
        if (dist<dist1):
            u,v=x1[i],y1[i]
            dist1=dist
    return u,v

r=int(input("Enter side length of hexagon"))
b=int(input("Enter the Breadth"))
l=int(input("Enter the Length"))
p=int(calculate_p(l, r))
o=int(calculate_o(b, r))
G=hexagonal_lattice_graph(o,p)
x,y=generate_hex_mesh(G)
x1,y1=generate_centers(x, y)
u,v=find_sink(b,l,x1,y1,r)

print(u,v)
plt.scatter(u,v)
plt.scatter(x,y)
#plt.scatter(x1,y1)
plt.show()
