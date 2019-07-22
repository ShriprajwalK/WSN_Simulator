"""Packet definition and properties."""


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
