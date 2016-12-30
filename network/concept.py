

class Concept(object):

    def __init__(self, name, semnet, parent=None, mods=None):
        self.name = name
        self.semnet = semnet
        self._attributes = {}
        self.mods = mods or []
        self.children = []
        self.parent = parent

    def _full_str(self, indent=0):
        ret = ["<%s '%s' %s>" % (self.__class__.__name__, self.name, self.mods)]
        for attr_name, attr_values in self.attributes.items():
            ret.append("|-" + attr_name + ":")

            for attr_val in attr_values[:-1]:
                if attr_val != self:
                    ret.append("|   " + attr_val.__repr__(indent + 1))

            if len(attr_values) > 0 and attr_values[-1] != self:
                ret.append("|   " + attr_values[-1].__repr__(indent + 1))

        return ("\n" + "|   "*indent).join(ret)

    def __repr__(self):
        return self._dot_label()

    def __getitem__(self, name):
        return self.attributes[name]

    def __setitem__(self, name, value):
        name = self.semnet.lemmatizer.lemmatize(name, pos="v")
        if name not in self._attributes:
            self._attributes[name] = []
        if value not in self._attributes[name]:
            self._attributes[name].append(value)
        return value

    def __hash__(self):
        return id(self)

    def decorate(self, mod, case=None):
        if type(mod) == str:
            mod = self.semnet.get(mod)
        if case is not None:
            mod = (mod, case)

        new_concept = Concept(self.name, self.semnet, self, self.mods + [mod])
        self.children.append(new_concept)

        return new_concept

    def _find_child(self, mods):
        all_mods_in_self = all([mod in self.mods for mod in mods])
        all_self_in_mods = all([mod in mods for mod in self.mods])

        if all_mods_in_self and all_self_in_mods:
            return self

        for child in self.children:
            found = child._find_child(mods)
            if found is not None:
                return found

        if not all_self_in_mods and self.parent is not None:
            return self.parent._find_child(mods)

        new_concept = Concept(self.name, self.semnet, self, mods)
        self.children.append(new_concept)
        return new_concept

    def _ref_count(self, ref_counts):
        for attr, objs in self._attributes.items():
            for obj in objs:
                if obj not in ref_counts:
                    ref_counts[obj] = 0
                ref_counts[obj] += 1
        for child in self.children:
            child._ref_count(ref_counts)
        return ref_counts


    def _dot_label(self):
        mods = [ "%s %s" % (mod[1], mod[0]._dot_label())
                 if type(mod) == tuple else mod._dot_label()
                 for mod in self.mods ]
        if len(mods) > 0:
            return self.name + '(' + ", ".join(mods) + ')'
        return self.name

    def _to_dot(self, ref_counts=None):
        node_label = self._dot_label()

        ret = []
        if ref_counts is None or self in ref_counts or len(self._attributes) > 0:
            if self.parent is not None:
                ret.append('"{}" -> "{}" [style=dotted]'.format(
                    node_label,
                    self.parent._dot_label()))

            for key, values in self._attributes.items():
                for value in values:
                    ret.append('"{}" -> "{}" [label="{}"]'.format(
                        node_label,
                        value._dot_label(),
                        key))

        for child in self.children:
            ret.append(child._to_dot(ref_counts))
        return '\n'.join(ret)

    def _to_list(self, ref_counts=None):
        node_label = self._dot_label()

        ret = []
        if ref_counts is None or self in ref_counts or len(self._attributes) > 0:
            if self.parent is not None:
                ret.append({
                    "source": node_label,
                    "target": self.parent._dot_label(),
                    "type": "<typeof>"})

            for key, values in self._attributes.items():
                for value in values:
                    ret.append({
                        "source": node_label,
                        "target": value._dot_label(),
                        "type": key})

        for child in self.children:
            ret += child._to_list(ref_counts)
        return ret

    @property
    def attributes(self):
        attrs = self.parent.attributes if self.parent is not None else {}
        attrs.update(self._attributes)
        return attrs

