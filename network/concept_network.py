
#from .concept import Concept
from concept import Concept

class ConceptNetwork(object):

    def __init__(self, stemmer=None):
        self._concepts = []
        self._stemmer = stemmer

    def get(self, name, amods=None):
        amods = amods or []

        if self._stemmer is not None:
            name = self._stemmer.stem(name)

        for concept in self._concepts:
            if concept.name == name:
                return concept._find_child(amods)

        new_concept = Concept(name)
        self._concepts.append(new_concept)
        return new_concept._find_child(amods)

    @property
    def concepts(self):
        return self._concepts

    def to_dot(self, filename):
        f = open(filename, 'w')
        f.write("digraph concept {\n")
        for concept in self._concepts:
            f.write(concept._to_dot())
            f.write('\n')
        f.write("\n}\n")
        f.close()

