from src import flow_graph

def main():
    g = flow_graph.FlowGraph('flow')
    for n in range(4):
        g.add_node(n)
    g.set_source(0)
    g.set_sink(3)
    g.add_edge(0, 1, 7)
    g.add_edge(0, 2, 5)
    g.add_edge(1, 2, 3)
    g.add_edge(1, 3, 5)
    g.add_edge(2, 3, 10)
    # print(g.edges)
    # print(g.rev_edges)
    g.validate()
    g.draw('orig')
    g.draw_res('orig res')
    g.add_flow(3, [0, 1, 3])
    g.validate()
    g.draw('add flow')
    g.draw_res('add flow res')


main()