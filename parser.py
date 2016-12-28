
from nltk.parse.dependencygraph import DependencyGraph
from nltk.parse.stanford import StanfordDependencyParser
from collections import defaultdict
import copy

import config

class Struct:
    def __init__(self, entries):
        self.__dict__.update(entries)
    def __repr__(self):
        return repr(self.__dict__)

_parser = StanfordDependencyParser(
    config.get("stanford", "jar-path"),
    config.get("stanford", "model-path"))

parse               = _parser.parse
parse_all           = _parser.parse_all
parse_one           = _parser.parse_one
parse_sents         = _parser.parse_sents
raw_parse           = _parser.raw_parse
raw_parse_sents     = _parser.raw_parse_sents
tagged_parse        = _parser.tagged_parse
tagged_parse_sents  = _parser.tagged_parse_sents

def connect_nodes(nodes):
    if type(nodes) == DependencyGraph:
        nodes = nodes.nodes
    nodes = copy.deepcopy(nodes)
    #dep_graph.nodes = { i: Struct(node) for i, node in dep_graph.nodes.items() }

    for i, node in nodes.items():
        if node["head"] is not None:
            node["head"] = nodes[node["head"]]

        for rel, dep_list in node["deps"].items():
            node["deps"][rel] = list(map(lambda i: nodes[i], dep_list))

    return nodes

