import os
import graphviz

class Edge:

    def __init__(self, n1: int, n2: int, c: int):
        self.n1 = n1
        self.n2 = n2
        self.c = c
        self.f_res_out = self.c
        self.f_res_in = 0

    def _check_flow_out(self, f_inc):
        assert f_inc <= self.f_res_out, f"illegal out flow increment {self.n1}->{self.n2}: {f_inc}"

    def _add_flow_out(self, f_inc):
        self._check_flow_out(f_inc)
        self.f_res_out -= f_inc
        self.f_res_in += f_inc
        print(f'adding out flow: {f_inc} to {self.n1}->{self.n2}')

    def _check_flow_in(self, f_inc):
        assert f_inc <= self.f_res_in, f"illegal in flow increment {self.n2}->{self.n1}: {f_inc}"

    def _add_flow_in(self, f_inc):
        self._check_flow_in(f_inc)
        self.f_res_in -= f_inc
        self.f_res_out += f_inc
        print(f'adding in flow: {f_inc} to {self.n2}->{self.n1}')

    def add_flow(self, n_from: int, n_to: int, f_inc: int, out_flow: bool):
        # out_flow = n_from == self.n1 and n_to == self.n2
        # in_flow = n_from == self.n2 and n_to == self.n1
        # out_flow = (n_from, n_to) in self.edg
        if out_flow:
            self._add_flow_out(f_inc)
        elif in_flow:
            self._add_flow_in(f_inc)
        else:
            raise AssertionError(f"cannot add flow from {n_from} to {n_to}, n1: {self.n1}, n2: {self.n2}")
        
    def get_out_flow(self):
        return self.c - self.f_res_out

    # def get_in_flow(self):
    #     return self.f_res_in

    def validate(self):
        assert self.f_res_out + self.f_res_in == self.c, f'f_res_in: {self.f_res_in} + f_res_out: {self.f_res_out} != c: {self.c}'

class FlowGraph:

    def __init__(self, name: str):
        self.name = name
        self.adj_lists = {}
        self.edges: dict[tuple[int, int], Edge] = {}
        self.source = -1
        self.sink = -1

    def add_node(self, n: int):
        assert n not in self.adj_lists, f"node {n} already stored"
        self.adj_lists[n] = []

    def add_edge(self, n1: int, n2: int, c: int):
        assert c > 0, f'capacity: {c} must be > 0'
        key = (n1, n2)
        assert key not in self.edges, f'key: {key} already stored'
        e = Edge(n1, n2, c)
        self.edges[key] = e
        self.adj_lists[n1].append(n2)
        self.adj_lists[n2].append(n1)

    # def get_edge_res_flow(self, n1: int, n2: int) -> int:
    #     assert n1 in self.adj_lists, f'node {n1} is not in the network'
    #     assert n2 in self.adj_lists, f'node {n2} is not in the network'
    #     if (n1, n2) in self.edges:
    #         flow = self.edges[(n1, n2)].get_out_flow()
    #     else:
    #         flow = self.edges[(n2, n1)].get_in_flow()
    #     return flow
    
    def set_source(self, source):
        self.source = source

    def set_sink(self, sink):
        self.sink = sink

    def add_flow(self, f_inc: int, nodes: list[int]):
        assert nodes[0] == self.source, f'node: {nodes[0]} != source: {self.source}'
        assert nodes[-1] == self.sink, f'node: {nodes[0]} != sink: {self.sink}'
        for index in range(1, len(nodes)):
            n1 = nodes[index-1]
            n2 = nodes[index]
            out_flow = (n1, n2) in self.edges
            if out_flow:
                self.edges[(n1, n2)]._add_flow_out(f_inc)
            else:
                self.edges[(n2, n1)]._add_flow_in(f_inc)

    def get_flow(self):
        out_flow_source = 0
        for n_to in self.adj_lists[self.source]:
            e = self.edges[(self.source, n_to)]
            f = e.get_out_flow()
            out_flow_source += f
        return out_flow_source
            
    def get_valid_nb_list(self, n_from) -> list[tuple[int, int]]:
        valid_nb_list = []
        for n_to in self.adj_lists[n_from]:
            if (n_from, n_to) in self.edges:
                flow = self.edges[(n_from, n_to)].f_res_out
            else:
                flow = self.edges[(n_to, n_from)].f_res_in
            # print(f'n_from: {n_from}, n_to: {n_to}, flow: {flow}')
            valid = flow > 0
            if valid:
                valid_nb_list.append((flow, n_to))
        return valid_nb_list

    # def _dfs_path_aux(self, path: list[tuple[None | int, int]], visited: list[bool], cur_min_flow: int | None) -> tuple[bool, int | None]:
    #     n_cur = path[-1][1]
    #     visited[n_cur] = True
    #     if n_cur == self.sink:
    #         return (True, cur_min_flow)
    #     flow_nb_list = self.get_valid_nb_list(n_cur)
    #     for flow, n_to in flow_nb_list:
    #         if not visited[n_to]:
    #             path.append((flow, n_to))
    #             if cur_min_flow is None or flow < cur_min_flow:
    #                 cur_min_flow = flow
    #             dest_found, next_min_flow = self._dfs_path_aux(path, visited, cur_min_flow)
    #             if dest_found:
    #                 return True, next_min_flow
    #             path.pop()
    #     return False, None

    # def find_dfs_path(self):
    #     path: list[tuple[None | int, int]] = [(None, self.source)]
    #     visited = [False] * len(self.adj_lists)
    #     dest_found, min_flow = self._dfs_path_aux(path, visited, None)
    #     if dest_found:
    #         return path, min_flow
    #     return [], None
    
    def _dfs_path_aux(self, path: list[int], visited: list[bool], min_flow: int) -> tuple[bool, int]:
        n_cur = path[-1]
        visited[n_cur] = True
        if n_cur == self.sink:
            return (True, min_flow)
        flow_nb_list = self.get_valid_nb_list(n_cur)
        for flow, n_to in flow_nb_list:
            if not visited[n_to]:
                path.append(n_to)
                cand_min_flow = min_flow
                if cand_min_flow == -1 or flow < cand_min_flow:
                    cand_min_flow = flow
                dest_found, next_min_flow = self._dfs_path_aux(path, visited, cand_min_flow)
                if dest_found:
                    return True, next_min_flow
                path.pop()
        return False, -1

    def find_dfs_path(self) -> tuple[list[int], int]:
        path = [self.source]
        visited = [False] * len(self.adj_lists)
        dest_found, min_flow = self._dfs_path_aux(path, visited, -1)
        if dest_found:
            return path, min_flow
        return [], -1

    def validate(self):
        for (n1, n2), e in self.edges.items():
            assert n1 == e.n1 and n2 == e.n2, f'illegal nodes in edge: {n1}, {n2}'
            e.validate()
        in_flow = {}
        out_flow = {}
        for n in self.adj_lists:
            out_flow[n] = 0
            in_flow[n] = 0
        for n_from, n_to_list in self.adj_lists.items():
            for n_to in n_to_list:
                if (n_from, n_to) in self.edges:
                    e = self.edges[(n_from, n_to)]
                    f = e.get_out_flow()
                    out_flow[n_from] += f
                    in_flow[n_to] += f
        for n, flow in out_flow.items():
            if n == self.source or n == self.sink:
                continue
            assert flow == in_flow[n], f'out flow and in flow from node {n} must be equal'
        assert in_flow[self.source] == 0, f'inflow to source {self.source} must be 0'
        assert out_flow[self.sink] == 0, f'outflow from sink {self.sink} must be 0'
        assert out_flow[self.source] == in_flow[self.sink], f"outflow from source {self.source} must be equal to inflow to sink: {self.sink}"
            

    def _add_graph_node(self, g: graphviz.Digraph, n: int):
        name = f'{n}'
        label = name
        if n == self.source:
            label += ' (s)'
        if n == self.sink:
            label += ' (d)'
        g.node(name=name, label=label)


    def draw(self, g_name: str = "flow"):
        img_format = 'png'
        g = graphviz.Digraph(format=img_format)
        label = f'{self.name}-{g_name}'
        g.attr(label=label)
        g.attr(labelloc='t')
        g.attr(splines='line')
        for n_from, n_to_list in self.adj_lists.items():
            self._add_graph_node(g, n_from)
            for n_to in n_to_list:
                if (n_from, n_to) in self.edges:
                    e = self.edges[(n_from, n_to)]
                    e_label = f'{e.get_out_flow()}/{e.c}'
                    g.edge(f'{n_from}', f'{n_to}', label=e_label)
        file_name_base = f'img/{label}'
        file_name = f'{file_name_base}.{img_format}'
        if os.path.exists(file_name):
            os.remove(file_name)
        g.render(file_name_base, view=True)

    def draw_res(self, g_name: str = "res"):
        img_format = 'png'
        g = graphviz.Digraph(format=img_format)
        label = f'{self.name}-{g_name}'
        g.attr(label=label)
        g.attr(labelloc='t')
        for n_from, n_to_list in self.adj_lists.items():
            self._add_graph_node(g, n_from)
            for n_to in n_to_list:
                if (n_from, n_to) in self.edges:
                    e = self.edges[(n_from, n_to)]
                    e_label = f'{e.f_res_out} (out) [{e.c}]'
                    g.edge(f'{n_from}', f'{n_to}', label=e_label)
                # if (n_to, n_from) in self.rev_edges:
                #     e = self.rev_edges[(n_to, n_from)]
                    e_rev_label = f'{e.f_res_in} (in)'
                    g.edge(f'{n_to}', f'{n_from}', label=e_rev_label)
        file_name_base = f'img/{label}'
        file_name = f'{file_name_base}.{img_format}'
        if os.path.exists(file_name):
            os.remove(file_name)
        g.render(file_name_base, view=True)

    