

class Concept(object):

    def __init__(self, name, parent=None, mods=None):
        self.name = name
        self._attributes = {}
        self.mods = mods or []
        self.children = []
        self.parent = parent

    def __repr__(self, indent=0):
        ret = ["%s <%s> %s" % (self.__class__.__name__, self.name, self.mods)]
        for attr_name, attr_values in self.attributes.items():
            ret.append("|-" + attr_name + ":")

            for attr_val in attr_values[:-1]:
                if attr_val != self:
                    ret.append("|   " + attr_val.__repr__(indent + 1))

            if len(attr_values) > 0 and attr_values[-1] != self:
                ret.append("|   " + attr_values[-1].__repr__(indent + 1))

        return ("\n" + "|   "*indent).join(ret)

    def __getitem__(self, name):
        return self.attributes[name]

    def __setitem__(self, name, value):
        if name not in self._attributes:
            self._attributes[name] = []
        if value not in self._attributes[name]:
            self._attributes[name].append(value)
        return value

    def _find_child(self, mods):
        all_mods_in_self = all([mod in self.mods for mod in mods])
        all_self_in_mods = all([mod in mods for mod in self.mods])

        if all_mods_in_self and all_self_in_mods:
            return self

        for child in self.children:
            found = child._find_child(mods)
            if found is not None:
                return found

        if all_self_in_mods:
            new_concept = Concept(self.name, self, mods)
            self.children.append(new_concept)
            return new_concept

        return None

    def _dot_label(self):
        return '"' + self.name + '(' + ", ".join(self.mods) + ')' + '"'

    def _to_dot(self, filename=None):
        node_label = self._dot_label()

        ret = []
        if self.parent is not None:
            ret.append(node_label + " -> " + self.parent._dot_label() +\
                        " [style=dotted]")

        for key, values in self._attributes.items():
            for value in values:
                ret.append(node_label + " -> " + value._dot_label() +\
                        " [label=\"" + key + "\"]")

        for child in self.children:
            ret.append(child._to_dot())
        return '\n'.join(ret)

    @property
    def attributes(self):
        attrs = self.parent.attributes if self.parent is not None else {}
        attrs.update(self._attributes)
        return attrs

