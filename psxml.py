class PrettySimpleXML():
    """A simple little pretty print XML generator."""
    def __init__(self, width=4):
        self._output = []
        self._open_tags = []
        self._width = " " * width
        self._depth = 0

    def _untrim(self, string, newline):
        """Inserts indentation and newline to a string."""
        if not isinstance(string, str):
            raise ValueError("first argument must be of type: string")
        if not isinstance(newline, bool):
            raise ValueError("second argument must be of type: boolean")
        lead = "" if not self._output or self._output[-1][-1] != "\n" else self._depth * self._width
        trail = "" if not newline else "\n"
        return lead + string + trail

    def _raw(self, string, newline):
        """Add a string exactly as given."""
        self._output.append(self._untrim(string, newline))
        return self

    def _empty(self, tag, attr, newline):
        """Add an empty element."""
        self._output.append(self._untrim("<{} />".format(" ".join([tag] + attr)), newline))
        return self

    def _begin(self, tag, attr, value, newline):
        """Begin and add a new element."""
        self._open_tags.append(tag)
        self._output.append(self._untrim("<{}>{}".format(" ".join([tag] + attr), value), newline))
        self._depth += 1
        return self

    def _end(self, newline):
        """End an element."""
        self._depth -= 1
        self._output.append(self._untrim("</{}>".format(self._open_tags.pop()), newline))
        return self

    def output(self):
        """Returns the output in pretty print."""
        return "".join(self._output)

    # convenience functions

    def raw(self, string):
        """Add a string exactly as given."""
        return self._raw(string, False)

    def rawln(self, string):
        """Add a string exactly as given and start a newline."""
        return self._raw(string, True)

    def empty(self, tag, attr=[]):
        """Add an empty element."""
        return self._empty(tag, attr, False)

    def emptyln(self, tag, attr=[]):
        """Add an empty element and start a newline."""
        return self._empty(tag, attr, True)

    def begin(self, tag, attr=[], value=""):
        """Begin and add a new element."""
        return self._begin(tag, attr, value, False)

    def beginln(self, tag, attr=[], value=""):
        """Begin, add a new element, and start a newline."""
        return self._begin(tag, attr, value, True)

    def end(self):
        """End an element."""
        return self._end(False)

    def endln(self):
        """End an element and start a newline."""
        return self._end(True)
