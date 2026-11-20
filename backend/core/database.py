import networkx as nx

class InMemoryDB:
    def __init__(self):
        self.G = nx.DiGraph()

    def clear(self):
        self.G.clear()

    def close(self):
        # Nothing to release for the in-memory graph (called on app shutdown).
        pass

db = InMemoryDB()
