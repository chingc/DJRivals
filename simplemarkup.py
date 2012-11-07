class SimpleMarkup():
    """A simple pretty print markup generator."""
    def __init__(self, width=4):
        self._output = []
        self._open_tags = []
        self._width = " " * width
        self._depth = 0

    def _check(self, value):
        """Raises ValueError if given is not a string."""
        if not isinstance(value, str):
            raise ValueError("must be of type string")
        return value

    def _check_attr(self, attr):
        """Raises ValueError if given is not a list of 2-tuple strings."""
        if not isinstance(attr, list):
            raise ValueError("must be of type list")
        for element in attr:
            if not isinstance(element, tuple) or len(element) != 2:
                raise ValueError("list elements must be a tuple of length 2")
        for name, value in attr:
            if not isinstance(name, str) or not isinstance(value, str):
                raise ValueError("tuple values must be of type string")
        return attr

    def _untrim(self, string, newline):
        """Inserts indentation and newline to a string."""
        lead = "" if not self._output or self._output[-1][-1] != "\n" else self._depth * self._width
        trail = "" if not newline else "\n"
        return lead + string + trail

    def _attr_str(self, attr):
        """Turns a list of attribute tuples into a string."""
        attribute = []
        for name, value in attr:
            attribute.append('{}="{}"'.format(name, value))
        return " " + " ".join(attribute) if len(attribute) > 0 else ""

    def _raw(self, string, newline):
        """Add a string exactly as given."""
        self._output.append(self._untrim(string, newline))
        return self

    def _empty(self, tag, attr, newline):
        """Add an empty element."""
        self._output.append(self._untrim("<{}{} />".format(tag, self._attr_str(attr)), newline))
        return self

    def _begin(self, tag, attr, value, newline):
        """Begin and add a new element."""
        self._open_tags.append(tag)
        self._output.append(self._untrim("<{}{}>{}".format(tag, self._attr_str(attr), value), newline))
        self._depth += 1
        return self

    def _end(self, newline):
        """End an element."""
        self._depth -= 1
        self._output.append(self._untrim("</{}>".format(self._open_tags.pop()), newline))
        return self

    # # # # #

    def output(self):
        """Returns the output in pretty print."""
        return "".join(self._output)

    def raw(self, string):
        """Add a string exactly as given."""
        return self._raw(self._check(string), False)

    def rawln(self, string):
        """Add a string exactly as given and start a newline."""
        return self._raw(self._check(string), True)

    def empty(self, tag, attr=[]):
        """Add an empty element."""
        return self._empty(self._check(tag), self._check_attr(attr), False)

    def emptyln(self, tag, attr=[]):
        """Add an empty element and start a newline."""
        return self._empty(self._check(tag), self._check_attr(attr), True)

    def begin(self, tag, attr=[], value=""):
        """Begin and add a new element."""
        return self._begin(self._check(tag), self._check_attr(attr), self._check(value), False)

    def beginln(self, tag, attr=[], value=""):
        """Begin, add a new element, and start a newline."""
        return self._begin(self._check(tag), self._check_attr(attr), self._check(value), True)

    def end(self):
        """End an element."""
        if self._depth == 0:
            raise IndexError("already ended")
        return self._end(False)

    def endln(self):
        """End an element and start a newline."""
        if self._depth == 0:
            raise IndexError("already ended")
        return self._end(True)
