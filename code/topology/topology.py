
set = frozenset

def bit(x, k):
    # Get the kth bit in the integer x
    return (x&(1 << k)) >> k


def AND(ints):
    # Return bitwise AND between all x in ints
    if len(ints)==0:
        return 0
    m = ints[0]
    for x in ints:
        m &= x
    return m

def OR(ints):
    # Return bitwise OR between all x in ints
    if len(ints)==0:
        return 0
    m = 0
    for x in ints:
        m |= x
    return m

set = frozenset

def bit(x, k):
    # Get the kth bit in the integer x
    return (x&(1 << k)) >> k

def AND(ints):
    # Return bitwise AND between all x in ints
    if len(ints)==0:
        return 0
    m = ints[0]
    for x in ints:
        m &= x
    return m

def OR(ints):
    # Return bitwise OR between all x in ints
    if len(ints)==0:
        return 0
    m = 0
    for x in ints:
        m |= x
    return m

def all_intersections(E ):
    # E is a set of subsets of some set, in their 'index representation', return all intersetcions of those sets.
    return set([ AND([i for j,i in enumerate(E) if bit(k,j) ]) for k in range(2**len(E)) ])

def all_unions(E ):
    # E is a set of subsets of some set, in their 'index representation', return all unions of those sets.
    return set([ OR([i for j,i in enumerate(E) if bit(k,j) ]) for k in range(2**len(E)) ])


def gen_topology(seed_set):
    X = set.union(*[set(x) for x in seed_set])
    X = [x for x in X]
    
    indexes = [ sum([ 2**X.index(x) for x in E ]) for E in seed_set]
    
    index_top = all_unions(all_intersections(indexes))
    
    top = [ [ x for j,x in enumerate(X) if bit(I,j) ] for I in index_top ]
    
    return index_top, top
    









"""
# Let the seed set be the set of subsets of X such that X = union(seed set)
# Then construct toppology from seed set.
# Need to generate set of all seed sets.

# To generate the power set of a set of n elemnets, \{x_1, ..., x_n\},
# generate all integers 0 <= k < n, in binary representation, 
# and let the jth bit of k decide if x_j is included in a union over j.

# To generate the set of all seed sets, generate the power set of X,
# then, iteratively, 
"""



    


















def all_intersections(E ):
    # E is a set of subsets of some set, in their 'index representation', return all intersetcions of those sets.
    return set([ AND([i for j,i in enumerate(E) if bit(k,j) ]) for k in range(2**len(E)) ])

def all_unions(E ):
    # E is a set of subsets of some set, in their 'index representation', return all unions of those sets.
    return set([ OR([i for j,i in enumerate(E) if bit(k,j) ]) for k in range(2**len(E)) ])


def gen_topology(seed_set):
    X = set.union(*[set(x) for x in seed_set])
    X = [x for x in X]
    
    indexes = [ sum([ 2**X.index(x) for x in E ]) for E in seed_set]
    
    index_top = all_unions(all_intersections(indexes))

    top = [ [ x for j,x in enumerate(X) if bit(I,j) ] for I in index_top ]
    
    return index_top, top
    









"""
# Let the seed set be the set of subsets of X such that X = union(seed set)
# Then construct toppology from seed set.
# Need to generate set of all seed sets.

# To generate the power set of a set of n elemnets, \{x_1, ..., x_n\},
# generate all integers 0 <= k < n, in binary representation, 
# and let the jth bit of k decide if x_j is included in a union over j.

# To generate the set of all seed sets, generate the power set of X,
# then, iteratively, 
"""



    

















