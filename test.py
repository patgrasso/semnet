
import sys

from assimilation import Assimilator
from concept import ConceptMap
import parser


mind = ConceptMap()
handler = Assimilator(mind)

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
                mind.to_dot(fname)
        else:
            dep_graph = parse(sentence)

            for a, rel, b in dep_graph.triples():
                print("{}({} <- {})".format(rel, a[0], b[0]))

            for i, node in dep_graph.nodes.items():
                print(i, { key: val for key, val in node.items()
                           if key in ["rel", "word", "deps", "tag"] })

repl()
