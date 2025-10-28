import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import math
import numpy as np

# Qiskit simulator imports
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit

# SciPy optional for local refinement
try:
    from scipy.optimize import minimize
    _HAS_SCIPY = True
except Exception:
    _HAS_SCIPY = False

# For Theorem 1 reference (analytical p=1 formula) we use the max-cut paper.
# See: Quantum Approximate Optimization Algorithm for MaxCut: A Fermionic View.
# Impl below follows Theorem 1 for <C_uv> (edge-level) and sums over edges.


class GraphLib:
    def __init__(self):
        self.G = nx.Graph()

    # ------------------------
    # Basic graph utilities
    # ------------------------
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
        return nx.is_complete(self.G)

    def visualize(self, with_labels=True, figsize=(6, 6), pos=None):
        """Matplotlib visualization (NetworkX spring layout by default)."""
        if pos is None:
            pos = nx.spring_layout(self.G, seed=42)
        plt.figure(figsize=figsize)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw(self.G, pos, with_labels=with_labels,
                node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()

    # ------------------------
    # Classical Max-Cut methods
    # ------------------------
    def max_cut_bruteforce(self):
        nodes = list(self.G.nodes())
        best_cut = None
        best_weight = -1
        for bits in itertools.product([0, 1], repeat=len(nodes)):
            S = {nodes[i] for i in range(len(nodes)) if bits[i] == 0}
            T = set(nodes) - S
            cut_weight = nx.cut_size(self.G, S, T, weight='weight')
            if cut_weight > best_weight:
                best_weight = cut_weight
                best_cut = (S, T)
        return best_cut, best_weight

    def max_cut_random(self, trials=1000):
        nodes = list(self.G.nodes())
        best_cut = None
        best_weight = -1
        for _ in range(trials):
            k = len(nodes)//2
            # allow variable split sometimes
            k = random.choice([k, max(1, k-1), min(len(nodes)-1, k+1)])
            S = set(random.sample(nodes, k=k))
            T = set(nodes) - S
            cut_weight = nx.cut_size(self.G, S, T, weight='weight')
            if cut_weight > best_weight:
                best_weight = cut_weight
                best_cut = (S, T)
        return best_cut, best_weight

    def max_cut_local_search(self, iterations=100):
        nodes = list(self.G.nodes())
        S = set(random.sample(nodes, k=len(nodes)//2))
        T = set(nodes) - S

        def cut_weight(S, T):
            return nx.cut_size(self.G, S, T, weight='weight')

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

    # ------------------------
    # Classical TSP methods
    # ------------------------
    def tsp_bruteforce(self):
        nodes = list(self.G.nodes())
        best_path = None
        best_cost = float('inf')
        for perm in itertools.permutations(nodes):
            # cost only defined if graph is complete between consecutive nodes
            try:
                cost = sum(self.G[perm[i]][perm[i+1]]['weight']
                           for i in range(len(perm)-1))
                cost += self.G[perm[-1]][perm[0]]['weight']
            except KeyError:
                continue
            if cost < best_cost:
                best_cost = cost
                best_path = perm
        return best_path, best_cost

    def tsp_nearest_neighbor(self, start=None):
        if start is None:
            start = next(iter(self.G.nodes()))
        nodes = set(self.G.nodes())
        path = [start]
        nodes.remove(start)
        total_cost = 0
        while nodes:
            last = path[-1]
            # choose neighbor among remaining nodes that has an edge.
            # if missing edges, break.
            candidates = [n for n in nodes if self.G.has_edge(last, n)]
            if not candidates:
                # cannot finish tour
                return None, float('inf')
            next_node = min(
                candidates, key=lambda x: self.G[last][x]['weight'])
            total_cost += self.G[last][next_node]['weight']
            path.append(next_node)
            nodes.remove(next_node)
        # close loop
        if not self.G.has_edge(path[-1], path[0]):
            return None, float('inf')
        total_cost += self.G[path[-1]][path[0]]['weight']
        return path, total_cost

    def tsp_mst_approximation(self):
        if not nx.is_connected(self.G):
            # MST undefined for disconnected graph
            return None, float('inf')
        mst = nx.minimum_spanning_tree(self.G)
        preorder_nodes = list(nx.dfs_preorder_nodes(
            mst, source=next(iter(self.G.nodes()))))
        total_cost = 0
        for i in range(len(preorder_nodes) - 1):
            total_cost += self.G[preorder_nodes[i]
                                 ][preorder_nodes[i+1]]['weight']
        total_cost += self.G[preorder_nodes[-1]][preorder_nodes[0]]['weight']
        return preorder_nodes, total_cost

    # ------------------------
    # QAOA p=1 utilities for MaxCut
    # ------------------------
    def _node_index_map(self):
        nodes = list(self.G.nodes())
        return {nodes[i]: i for i in range(len(nodes))}, nodes

    def build_qaoa1_circuit(self, gamma, beta):
        """
        Build a QAOA p=1 circuit for MaxCut on self.G.
        Uses RZZ-like two-qubit phase (via controlled-RZ pattern) and RX for mixer.
        Returns a QuantumCircuit without measurements.
        """
        n = self.G.number_of_nodes()
        if n == 0:
            raise ValueError("Graph is empty.")
        idx_map, _ = self._node_index_map()
        qc = QuantumCircuit(n)
        qc.h(range(n))
        # cost: for each edge apply RZZ via two CNOTs + RZ + CNOT (works for Aer)
        for (u, v, data) in self.G.edges(data=True):
            w = data.get('weight', 1)
            i = idx_map[u]
            j = idx_map[v]
            angle = 2.0 * gamma * w  # convention
            angle = 2.0 * gamma * w
            # implement e^{-i angle/2 Z_i Z_j} with CNOT-RZ-CNOT
            qc.cx(i, j)
            qc.rz(angle, j)
            qc.cx(i, j)
        # mixer
        for q in range(n):
            qc.rx(2.0 * beta, q)
        return qc

    def qaoa1_expectation_classical(self, gamma, beta):
        """
        Analytic p=1 expectation using Theorem 1-like formula (edge-local).
        Fast and independent of Qiskit execution. Returns expected cut-value.
        """
        total = 0.0
        for (u, v, data) in self.G.edges(data=True):
            w = data.get('weight', 1)
            du = self.G.degree(u) - 1
            dv = self.G.degree(v) - 1
            lam = len(list(nx.common_neighbors(self.G, u, v)))

            sin4b = math.sin(4.0 * beta)
            sin2b_sq = math.sin(2.0 * beta) ** 2
            cos_g = math.cos(gamma)
            cos_2g = math.cos(2.0 * gamma)

            cos_du = cos_g ** du if du >= 0 else 1.0
            cos_dv = cos_g ** dv if dv >= 0 else 1.0
            cos_du_dv_2lam = cos_g ** (du + dv - 2 * lam) if (du + dv - 2 * lam) >= 0 else 1.0
            cos_2g_pow_lam = cos_2g ** lam if lam >= 0 else 1.0

            term = (
                0.5
                + 0.25 * (sin4b * math.sin(gamma)) * (cos_du + cos_dv)
                - 0.25 * (sin2b_sq * cos_du_dv_2lam) * (1.0 - cos_2g_pow_lam)
            )
            total += w * term
        return total

    def qaoa1_expectation_simulated(self, gamma, beta, shots=1024, backend=None):
        """
        Build QAOA1 circuit, measure, run on AerSimulator (or provided backend),
        return expectation and best sampled bitstring info.
        """
        if backend is None:
            backend = AerSimulator()
        qc = self.build_qaoa1_circuit(gamma, beta)
        # measurement
        qc_meas = qc.copy()
        qc_meas.measure_all()
        # transpile for AerSimulator
        transpiled = transpile(qc_meas, backend=backend, optimization_level=1)
        job = backend.run(transpiled, shots=shots)
        result = job.result()
        counts = result.get_counts()

        # compute cut from bitstring (qiskit returns bitstrings MSB..LSB; map with reverse)
        idx_map, _ = self._node_index_map()

        def cut_value_from_bitstring(bitstr):
            b_rev = bitstr[::-1]
            cut = 0
            for (u, v, data) in self.G.edges(data=True):
                i = idx_map[u]
                j = idx_map[v]
                bu = int(b_rev[i])
                bv = int(b_rev[j])
                if bu != bv:
                    cut += data.get('weight', 1)
            return cut

        total = 0.0
        best_cut = -1
        best_bs = None
        for bs, cnt in counts.items():
            val = cut_value_from_bitstring(bs)
            total += val * cnt
            if val > best_cut:
                best_cut = val
                best_bs = bs
        expectation = total / shots
        return {
            'expectation': expectation,
            'best_bitstring': best_bs,
            'best_cut': best_cut,
            'counts': counts,
            'shots': shots
        }

    def optimize_qaoa1_classical(self, grid_res=41, gamma_bounds=(0, math.pi/2), beta_bounds=(0, math.pi/2), refine=True):
        """
        Coarse grid search on analytic objective, optional refine with SciPy COBYLA.
        Returns best (gamma, beta, value, refine_info).
        """
        g_grid = np.linspace(gamma_bounds[0], gamma_bounds[1], grid_res)
        b_grid = np.linspace(beta_bounds[0], beta_bounds[1], grid_res)
        best_val = -1e9
        best_pair = (None, None)
        for g in g_grid:
            for b in b_grid:
                val = self.qaoa1_expectation_classical(g, b)
                if val > best_val:
                    best_val = val
                    best_pair = (g, b)
        refine_info = None
        if refine and _HAS_SCIPY and best_pair[0] is not None:
            def neg_obj(x):
                return -self.qaoa1_expectation_classical(float(x[0]), float(x[1]))
            x0 = np.array(best_pair)
            res = minimize(neg_obj, x0=x0, method='COBYLA',
                           options={'maxiter': 200})
            best_gamma, best_beta = float(res.x[0]), float(res.x[1])
            best_val = -res.fun
            refine_info = {'success': res.success, 'message': res.message}
        else:
            best_gamma, best_beta = best_pair
        return best_gamma, best_beta, best_val, refine_info
