
from .concept import Concept
from nltk.stem import WordNetLemmatizer

class SemNet(object):

    def __init__(self):
        self.concepts = []
        self.lemmatizer = WordNetLemmatizer()

    def get(self, name, mods=None):
        """
        Retrieves a concept by name from the network with modifiers

        @param name: str
        @param mods: [str | (str, str)]

        @return network.Concept
        """
        mods = mods or []

        name = self.lemmatizer.lemmatize(name)

        for concept in self.concepts:
            if concept.name == name:
                return concept._find_child(mods)

        new_concept = Concept(name, self)
        self.concepts.append(new_concept)
        return new_concept._find_child(mods)

    def to_dot(self, filename):
        f = open(filename, 'w')
        f.write("digraph semnet {\n")

        ref_counts = {}
        for concept in self.concepts:
            concept._ref_count(ref_counts)

        for concept in self.concepts:
            f.write(concept._to_dot(ref_counts))
            f.write('\n')

        f.write("\n}\n")
        f.close()

