class PrettySimpleXML():
    """A simple little pretty print XML generator."""
    def __init__(self, width=4):
        self._output = []
        self._open_tags = []
        self._width = " " * width
        self._depth = 0

    def _untrim(self, value, newline):
        lead = "" if not self._output or self._output[-1][-1] != "\n" else self._depth * self._width
        trail = "" if not newline else "\n"
        return "{}{}{}".format(lead, value, trail)

    def get(self):
        return "".join(self._output)

    def raw(self, value, newline=True):
        self._output.append(self._untrim(value, newline))
        return self

    def empty(self, tag, attr=[], newline=True):
        self._output.append(self._untrim("<{} />".format(" ".join([tag] + attr)), newline))
        return self

    def start(self, tag, attr=[], value="", newline=True):
        self._open_tags.append(tag)
        self._output.append(self._untrim("<{}>{}".format(" ".join([tag] + attr), value), newline))
        self._depth += 1
        return self

    def end(self, newline=True):
        self._depth -= 1
        self._output.append(self._untrim("</{}>".format(self._open_tags.pop()), newline))
        return self

    def end_all(self):
        while len(self._open_tags):
            self.end()
        return self
