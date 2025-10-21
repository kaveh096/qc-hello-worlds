import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools


class GraphLib:
    def __init__(self):
        self.G = nx.Graph()

    def add_vertex(self, v):
        self.G.add_node(v)

    def add_edge(self, u, v, weight=1):
        self.G.add_edge(u, v, weight=weight)

    def generate_random_graph(
        self, num_vertices, edge_prob=0.3, weight_range=(1, 10), seed=None
    ):
        """Generate an undirected weighted Erdős–Rényi random graph."""
        self.G = nx.erdos_renyi_graph(num_vertices, edge_prob, seed=seed)
        for (u, v) in self.G.edges():
            self.G[u][v]['weight'] = random.randint(*weight_range)
        return self.G

    def create_path_from_vertices(self, vertices, weight_range=(1, 10)):
        """Add edges in order of given vertices to form a path."""
        for i in range(len(vertices) - 1):
            if not self.G.has_edge(vertices[i], vertices[i+1]):
                w = random.randint(*weight_range)
                self.add_edge(vertices[i], vertices[i+1], w)

    def is_complete(self):
        """Return True if the graph is a complete graph."""
        n = self.G.number_of_nodes()
        # A complete undirected graph has n*(n-1)/2 edges
        expected_edges = n * (n - 1) // 2
        return self.G.number_of_edges() == expected_edges

    def visualize(self, with_labels=True):
        pos = nx.spring_layout(self.G)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw(self.G, pos, with_labels=with_labels,
                node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()

    # ===== MAX-CUT =====
    def max_cut_bruteforce(self):
        nodes = list(self.G.nodes())
        best_cut = None
        best_weight = -1
        for bits in itertools.product([0, 1], repeat=len(nodes)):
            S = {nodes[i] for i in range(len(nodes)) if bits[i] == 0}
            T = set(nodes) - S
            cut_weight = sum(
                self.G[u][v]['weight']
                for u, v in self.G.edges()
                if (u in S and v in T) or (u in T and v in S)
            )
            if cut_weight > best_weight:
                best_weight = cut_weight
                best_cut = (S, T)
        return best_cut, best_weight

    def max_cut_random(self, trials=1000):
        nodes = list(self.G.nodes())
        best_cut = None
        best_weight = -1
        for _ in range(trials):
            S = set(random.sample(nodes, k=len(nodes)//2))
            T = set(nodes) - S
            cut_weight = sum(
                self.G[u][v]['weight']
                for u, v in self.G.edges()
                if (u in S and v in T) or (u in T and v in S)
            )
            if cut_weight > best_weight:
                best_weight = cut_weight
                best_cut = (S, T)
        return best_cut, best_weight

    def max_cut_local_search(self, iterations=100):
        nodes = list(self.G.nodes())
        S = set(random.sample(nodes, k=len(nodes)//2))
        T = set(nodes) - S

        def cut_weight(S, T):
            return sum(
                self.G[u][v]['weight']
                for u, v in self.G.edges()
                if (u in S and v in T) or (u in T and v in S)
            )

        best_weight = cut_weight(S, T)
        for _ in range(iterations):
            improved = False
            for node in list(S):
                S.remove(node)
                T.add(node)
                new_weight = cut_weight(S, T)
                if new_weight > best_weight:
                    best_weight = new_weight
                    improved = True
                    break
                else:
                    T.remove(node)
                    S.add(node)
            if not improved:
                break
        return (S, T), best_weight

    # ===== TSP =====
    def tsp_bruteforce(self):
        nodes = list(self.G.nodes())
        best_path = None
        best_cost = float('inf')
        for perm in itertools.permutations(nodes):
            cost = sum(self.G[perm[i]][perm[i+1]]['weight']
                       for i in range(len(perm)-1))
            cost += self.G[perm[-1]][perm[0]]['weight']  # return to start
            if cost < best_cost:
                best_cost = cost
                best_path = perm
        return best_path, best_cost

    def tsp_nearest_neighbor(self, start=0):
        nodes = set(self.G.nodes())
        path = [start]
        nodes.remove(start)
        total_cost = 0
        while nodes:
            last = path[-1]
            next_node = min(nodes, key=lambda x: self.G[last][x]['weight'])
            total_cost += self.G[last][next_node]['weight']
            path.append(next_node)
            nodes.remove(next_node)
        total_cost += self.G[path[-1]][path[0]]['weight']  # close loop
        return path, total_cost

    def tsp_mst_approximation(self):
        mst = nx.minimum_spanning_tree(self.G)
        preorder_nodes = list(nx.dfs_preorder_nodes(mst, source=0))
        total_cost = 0
        for i in range(len(preorder_nodes) - 1):
            total_cost += self.G[preorder_nodes[i]
                                 ][preorder_nodes[i+1]]['weight']
        total_cost += self.G[preorder_nodes[-1]][preorder_nodes[0]]['weight']
        return preorder_nodes, total_cost
