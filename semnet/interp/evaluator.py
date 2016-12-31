

class Evaluator(object):

    def __init__(self, env):
        self.env = env

    def valueof(self, node, node_list):
        self.env.get(node["word"])


