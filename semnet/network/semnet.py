
from semnet.network import Concept
from semnet.observer import Observable
from nltk.stem import WordNetLemmatizer

class SemNet(Observable):

    def __init__(self):
        super(SemNet, self).__init__()
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
        self.emit("new_concept", concept=new_concept)

        return new_concept._find_child(mods)

    def to_dot(self, filename=None, topics=None):
        content = "digraph semnet {\n"

        ref_counts = {}
        for concept in self.concepts:
            concept._ref_count(ref_counts)

        for concept in self.concepts:
            if topics is None or concept.name in topics:
                content += concept._to_dot(ref_counts)
                content += '\n'

        content += "\n}\n"

        if filename is not None:
            f = open(filename, 'w')
            f.write(content)
            f.close()
        return content

    def to_list(self):
        relations = []

        ref_counts = {}
        for concept in self.concepts:
            concept._ref_count(ref_counts)

        for concept in self.concepts:
            relations += concept._to_list(ref_counts)

        return relations

