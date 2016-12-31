
from .evaluator import Evaluator

class CopEvaluator(Evaluator):

    def valueof(self, node, node_list):
        verb = self.env.get(node["word"])

        subj = something["nsubj"].valueof(
            node_list[node_list[node["head"]]["deps"]["nsubj"][0]],
            node_list)

        pred = valueof(node_list[node["head"]], node_list)
