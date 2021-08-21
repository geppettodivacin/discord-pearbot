from collections import namedtuple

Result = namedtuple('Result', ['pairs', 'leftovers'])

def compute(members):
    # TODO: Actually use roles to pair
    mid = (len(members) // 2)
    pairs = zip(members[:mid], members[mid:])
    leftovers = [] if len(members) % 2 == 0 else [members[-1]]
    return Result(pairs = pairs, leftovers = leftovers)
