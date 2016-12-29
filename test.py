
import sys, os

from network import SemNet
import interp
import parser
import config


mind = SemNet()

def show_concept(concept=None):
    if concept is None:
        for c in mind.concepts:
            print(c)
            print()
    else:
        print(concept)
        print()
        for child in concept.children:
            show_concept(child)

def parse(sentence):
    dep_graph = next(parser.raw_parse(sentence))
    #nodes = parser.connect_nodes(dep_graph)
    #handler.assimilate(nodes[0])
    interp.eval_root(dep_graph.root, dep_graph.nodes, mind)
    return dep_graph

def repl():
    while True:
        sys.stdout.write("--> ")
        sentence = input()
        if sentence.startswith("show"):
            query = (sentence.split(' ') + [None])[1]
            query = mind.get(query) if query is not None else None
            show_concept(query)
        elif sentence.startswith("dot"):
            fname = (sentence.split(' ') + [None])[1]
            if fname is not None:
                mind.to_dot(os.path.join(
                    config.get("graphs", "output-dir"),
                    fname))
        else:
            dep_graph = parse(sentence)

            for a, rel, b in dep_graph.triples():
                print("{}({} <- {})".format(rel, a[0], b[0]))

            for i, node in dep_graph.nodes.items():
                print(i, { key: val for key, val in node.items()
                           if key in ["rel", "word", "deps", "tag"] })

#parse("a tree is a tall plant with a trunk and branches made of wood")
#parse("the oldest tree ever discovered is approximately 5,000 years old")

repl()
