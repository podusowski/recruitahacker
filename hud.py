_parts = []
_named_values = {}


class NamedValue:
    def __init__(self, name):
        self.name = name
        self.value = None

    def __str__(self):
        return '{}: {}'.format(self.name, self.value)


def add(part):
    _parts.append(part)

def render():
    print(' | '.join(_parts + list(_named_values)), end='\r')

def inc(name):
    if not name in _named_values:
        _named_values[name] = 0
    _named_values[name] += 1
