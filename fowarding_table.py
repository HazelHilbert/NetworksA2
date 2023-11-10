class ForwardingTable:
    def __init__(self):
        self.forwarding_table = []

    def add_entry(self, destination, next_hop, timer):
        entry = ForwardingTableEntry(destination, next_hop, timer)
        self.forwarding_table.append(entry)

    def remove_entry(self, destination):
        self.forwarding_table = [entry for entry in self.forwarding_table if entry.destination != destination]

    def get_next_hop(self, destination_address):
        for entry in self.forwarding_table:
            if entry.destination == destination_address:
                return entry.next_hop
        return None

    def __str__(self):
        return "\n".join(str(entry) for entry in self.forwarding_table)


class ForwardingTableEntry:
    def __init__(self, destination, next_hop, timer):
        self.destination = destination
        self.next_hop = next_hop
        self.timer = timer

    def __str__(self):
        return f"Destination: {self.destination}, Next Hop: {self.next_hop}, Timer: {self.timer}"
