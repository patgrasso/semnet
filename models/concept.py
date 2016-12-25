
concepts = []

class Concept(object):

    def __init__(self, name):
        self.name = name
        self.attributes = {}
        self.instances = []

        concepts.append(self)

    def __repr__(self, indent=0):
        ret = ["%s <%s>" % (self.__class__.__name__, self.name)]
        for attr_name, attr_values in self.attributes.items():
            ret.append("  " + attr_name + ": ")
            for attr_val in attr_values:
                ret.append("    " + attr_val.__repr__(indent + 1))
        return ("\n" + "    "*indent).join(ret)

    def __getitem__(self, name):
        return self.attributes[name]

    def __setitem__(self, name, value):
        if name not in self.attributes:
            self.attributes[name] = []
        self.attributes[name].append(value)
        return self

    @staticmethod
    def get(name):
        for concept in concepts:
            if concept.name == name:
                return concept
        new_concept = Concept(name)
        concepts.append(new_concept)
        return new_concept

    @staticmethod
    def concepts():
        return concepts

