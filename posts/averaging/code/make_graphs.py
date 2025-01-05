import graphviz


def make_line():
    dot = graphviz.Graph()
    dot.node('1')
    dot.node('2')
    dot.edge('1', '2')
    dot.render('line.gv', format='png')


def make_star():
    dot = graphviz.Graph()
    dot.node('1')
    dot.node('2')
    dot.node('3')
    dot.node('4')
    dot.node('5')
    dot.edge('1', '2')
    dot.edge('1', '3')
    dot.edge('1', '4')
    dot.edge('1', '5')
    dot.render('star.gv', format='png')


def main():
    make_line()
    make_star()


main()
