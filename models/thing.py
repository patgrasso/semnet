
from .concept import Concept

class Thing(Concept):

    def __init__(self, parent, mods=None):
        super(Thing, self).__init__(parent.name)
        self.parent = parent
        self.mods = mods or []

    def __repr__(self, indent=0):
        ret = super(Thing, self).__repr__(indent).split("\n")
        ret = ["%s <%s> %s" % (self.__class__.__name__,
                               self.parent.name,
                               self.mods)] + ret
        return '\n'.join(ret)

    @staticmethod
    def get(name, mods=None):
        abstract = Concept.get(name)
        if mods is not None and mods != []:
            return Thing(abstract, mods)
        return abstract

