
from .evaluator import Evaluator

class RootEvaluator(Evaluator):

    def valueof(self, node, node_list):
        for rel, dep_nodes in node["deps"].items():
            for dep_node in dep_nodes:
                something[rel].valueof(node_list[dep_node], node_list)
