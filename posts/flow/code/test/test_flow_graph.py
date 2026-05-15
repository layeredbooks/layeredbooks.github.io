import unittest
import warnings
import os

from src import flow_graph

DRAW_ENABLED = os.getenv('FLOW_DRAW') == '1'

def _make_four_nodes() -> flow_graph.FlowGraph:
    g = flow_graph.FlowGraph("four")
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.set_source(0)
    g.set_sink(3)
    g.add_edge(0, 1, 6)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 2, 2)
    g.add_edge(1, 3, 3)
    g.add_edge(2, 3, 6)
    g.validate()
    return g

class TestFlowGraph(unittest.TestCase):
    
    def _make_two_nodes(self) -> flow_graph.FlowGraph:
        g = flow_graph.FlowGraph("two")
        g.add_node(0)
        g.add_node(1)
        g.set_source(0)
        g.set_sink(1)
        g.add_edge(0, 1, 5)
        g.validate()
        return g

    def test_draw_two_nodes(self):
        if not DRAW_ENABLED:
            return
        g = self._make_two_nodes()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning) 
            g.draw("orig")
            g.draw_res("res")
        f_add = 4
        g.add_flow(f_add, [0, 1])
        g.validate()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning) 
            g.draw("orig-add")
            g.draw_res("res-add")

    def test_two_nodes(self):
        g = self._make_two_nodes()
        f_add = 3
        g.add_flow(f_add, [0, 1])
        g.validate()
        f = g.get_flow()
        self.assertEqual(f, f_add)
        f_add_rev = 1
        e = g.edges[(0, 1)]
        e._add_flow_in(f_add_rev) # (1, 0, f_add_rev)
        g.validate()
        f = g.get_flow()
        self.assertEqual(f, f_add-f_add_rev)

    def _make_three_nodes(self) -> flow_graph.FlowGraph:
        g = flow_graph.FlowGraph("three")
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.set_source(0)
        g.set_sink(2)
        g.add_edge(0, 1, 3)
        g.add_edge(1, 2, 5)
        g.validate()
        return g

    def test_draw_three_nodes(self):
        if not DRAW_ENABLED:
            return
        g = self._make_three_nodes()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning) 
            g.draw("orig")
            g.draw_res("res")
        f_add = 2
        g.add_flow(f_add, [0, 1, 2])
        g.validate()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning) 
            g.draw("orig-add")
            g.draw_res("res-add")

    def test_three_nodes(self):
        g = self._make_three_nodes()
        f_add = 2
        g.add_flow(f_add, [0, 1, 2])
        g.validate()
        f = g.get_flow()
        self.assertEqual(f, f_add)
        f_add_rev = 1
        e = g.edges[(0, 1)]
        e._add_flow_in(f_add_rev) # (1, 0, f_add_rev)
        e = g.edges[(1, 2)]
        e._add_flow_in(f_add_rev) # (2, 1, f_add_rev)
        g.validate()
        f = g.get_flow()
        self.assertEqual(f, f_add-f_add_rev)

    def test_draw_four_nodes(self):
        if not DRAW_ENABLED:
            return
        g = _make_four_nodes()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning) 
            g.draw("orig")
            g.draw_res("res")
        f_add = 2
        g.add_flow(f_add, [0, 1, 3])
        g.validate()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning) 
            g.draw("orig-add")
            g.draw_res("res-add")

    def test_four_nodes(self):
        g = _make_four_nodes()
        g.add_flow(3, [0, 1, 3])
        g.validate()
        self.assertEqual(g.get_flow(), 3)
        e = g.edges[(0, 1)]
        e._add_flow_in(1) # (1, 0, 1)
        e = g.edges[(1, 3)]
        e._add_flow_in(1) # (3, 1, 1)
        g.validate()
        self.assertEqual(g.get_flow(), 2)
        g.add_flow(1, [0, 1, 3])
        g.validate()
        self.assertEqual(g.get_flow(), 3)
        g.add_flow(3, [0, 2, 3])
        g.validate()
        self.assertEqual(g.get_flow(), 6)
        g.add_flow(2, [0, 1, 2, 3])
        g.validate()
        g.validate()
        self.assertEqual(g.get_flow(), 8)

    def test_valid_nb_list(self):
        g = _make_four_nodes()
        n_nodes = 4
        # ----------------------------------------------------- #
        n_valid = [2, 2, 1, 0]
        flow_and_dest = [[(6, 1), (3, 2)], [(2, 2), (3, 3)], [(6, 3)], []]
        for n in range(n_nodes):
            nb_list = g.get_valid_nb_list(n)
            self.assertEqual(len(nb_list), n_valid[n])
            self.assertEqual(nb_list, flow_and_dest[n])
        # ----------------------------------------------------- #
        g.add_flow(3, [0, 1, 3])
        g.validate()
        self.assertEqual(g.get_flow(), 3)
        n_valid = [2, 2, 1, 1]
        flow_and_dest = [[(3, 1), (3, 2)], [(3, 0), (2, 2)], [(6, 3)], [(3, 1)]]
        for n in range(n_nodes):
            nb_list = g.get_valid_nb_list(n)
            self.assertEqual(len(nb_list), n_valid[n])
            self.assertEqual(nb_list, flow_and_dest[n])
        # ----------------------------------------------------- #
        e = g.edges[(0, 1)]
        e._add_flow_in(1) # , 0, 1)
        e = g.edges[(1, 3)]
        e._add_flow_in(1) # tflow(3, 1, 1)
        g.validate()
        self.assertEqual(g.get_flow(), 2)
        n_valid = [2, 3, 1, 1]
        flow_and_dest = [[(4, 1), (3, 2)], [(2, 0), (2, 2), (1, 3)], [(6, 3)], [(2, 1)]]
        for n in range(n_nodes):
            nb_list = g.get_valid_nb_list(n)
            self.assertEqual(len(nb_list), n_valid[n])
            self.assertEqual(nb_list, flow_and_dest[n])
        # ----------------------------------------------------- #
        g.add_flow(1, [0, 1, 3])
        g.validate()
        self.assertEqual(g.get_flow(), 3)
        n_valid = [2, 2, 1, 1]
        flow_and_dest = [[(3, 1), (3, 2)], [(3, 0), (2, 2)], [(6, 3)], [(3, 1)]]
        for n in range(n_nodes):
            nb_list = g.get_valid_nb_list(n)
            self.assertEqual(len(nb_list), n_valid[n])
            self.assertEqual(nb_list, flow_and_dest[n])
        # ----------------------------------------------------- #
        g.add_flow(3, [0, 2, 3])
        g.validate()
        self.assertEqual(g.get_flow(), 6)
        n_valid = [1, 2, 2, 2]
        flow_and_dest = [[(3, 1)], [(3, 0), (2, 2)], [(3, 0), (3, 3)], [(3, 1), (3, 2)]]
        for n in range(n_nodes):
            nb_list = g.get_valid_nb_list(n)
            self.assertEqual(len(nb_list), n_valid[n])
            self.assertEqual(nb_list, flow_and_dest[n])
        # ----------------------------------------------------- #
        g.add_flow(2, [0, 1, 2, 3])
        g.validate()
        self.assertEqual(g.get_flow(), 8)
        n_valid = [1, 1, 3, 2]
        flow_and_dest = [[(1, 1)], [(5, 0)], [(3, 0), (2, 1), (1, 3)], [(3, 1), (5, 2)]]
        for n in range(n_nodes):
            nb_list = g.get_valid_nb_list(n)
            self.assertEqual(len(nb_list), n_valid[n])
            self.assertEqual(nb_list, flow_and_dest[n])

    def test_dfs_path(self):
        g = _make_four_nodes()
        tot_flow = 0
        # ----------------------------------------------------- #
        g.validate()
        path, min_flow = g.find_dfs_path()
        print(path, min_flow)
        tot_flow += min_flow
        self.assertEqual(len(path), 4)
        self.assertEqual(min_flow, 2)
        # ----------------------------------------------------- #
        g.add_flow(min_flow, path)
        g.validate()
        path, min_flow = g.find_dfs_path()
        print(path, min_flow)
        tot_flow += min_flow
        self.assertEqual(len(path), 3)
        self.assertEqual(min_flow, 3)
        # ----------------------------------------------------- #
        g.add_flow(min_flow, path)
        g.validate()
        path, min_flow = g.find_dfs_path()
        print(path, min_flow)
        tot_flow += min_flow
        self.assertEqual(len(path), 3)
        self.assertEqual(min_flow, 3)
        # ----------------------------------------------------- #
        g.add_flow(min_flow, path)
        g.validate()
        if DRAW_ENABLED:
            g.draw()
            g.draw_res()
        path, min_flow = g.find_dfs_path()
        print(path, min_flow)
        self.assertEqual(len(path), 0)
        self.assertEqual(min_flow, -1)
        # ----------------------------------------------------- #
        network_flow = g.get_flow()
        self.assertEqual(tot_flow, network_flow)
        return

def ford_fulkerson(g: flow_graph.FlowGraph) -> int:
    done = False
    while not done:
        path, min_flow = g.find_dfs_path()
        if min_flow != -1:
            g.add_flow(min_flow, path)
        else:
            done = True
    max_flow = g.get_flow()
    return max_flow
            

class TestFordFulkerson(unittest.TestCase):

    def test_four_nodes(self):
        g = _make_four_nodes()
        max_flow = ford_fulkerson(g)
        self.assertEqual(max_flow, 8)

    def test_add_in_flow(self):
        g = flow_graph.FlowGraph("add_in_flow")
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.set_source(0)
        g.set_sink(3)
        g.add_edge(0, 1, 3)
        g.add_edge(1, 2, 1)
        g.add_edge(1, 3, 3)
        g.add_edge(0, 2, 3)
        g.add_edge(2, 3, 3)
        g.validate()
        # g.draw()
        max_flow = ford_fulkerson(g)
        self.assertEqual(max_flow, 6)


