import  random
import deap
from deap import base
from deap import creator
from deap import tools


# tools.cxESTwoPoints()
IND_ROBNUM = 0
IND_TASKNUM = 0


def mpda_PMX_mate(ind1,ind2):
    for i  in  range(0,len(ind1),IND_TASKNUM):
        cxInd1 = ind1[i:i+IND_TASKNUM]
        cxInd2 = ind2[i:i+IND_TASKNUM]
        # print(cxInd1)
        # print(cxInd2)
        mpda_cxPartialyMatched(cxInd1,cxInd2)

        # print('change cxInd1 = ',cxInd1)
        # print('change cxInd2 = ',cxInd2)
        ind1[i:i + IND_TASKNUM] = cxInd1
        ind2[i:i + IND_TASKNUM] = cxInd2
        # print(ind1)
        # print(ind2)

    return ind1,ind2

def mpda_cxPartialyMatched(ind1, ind2):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.

    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes. For more details see [Goldberg1985]_.

    This function uses the :func:`~random.randint` function from the python base
    :mod:`random` module.

    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
       salesman problem", 1985.
    """
    size = min(len(ind1), len(ind2))
    p1, p2 = [0] * size, [0] * size

    # Initialize the position of each indices in the individuals
    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i
    # Choose crossover points
    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1, ind2



def cxOrdered(ind1, ind2):
    """Executes an ordered crossover (OX) on the input
    individuals. The two individuals are modified in place. This crossover
    expects :term:`sequence` individuals of indices, the result for any other
    type of individuals is unpredictable.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.

    Moreover, this crossover generates holes in the input
    individuals. A hole is created when an attribute of an individual is
    between the two crossover points of the other individual. Then it rotates
    the element so that all holes are between the crossover points and fills
    them with the removed elements in order. For more details see
    [Goldberg1989]_.

    This function uses the :func:`~random.sample` function from the python base
    :mod:`random` module.

    .. [Goldberg1989] Goldberg. Genetic algorithms in search,
       optimization and machine learning. Addison Wesley, 1989
    """
    size = min(len(ind1), len(ind2))
    a, b = random.sample(range(size), 2)
    if a > b:
        a, b = b, a

    holes1, holes2 = [True] * size, [True] * size
    for i in range(size):
        if i < a or i > b:
            holes1[ind2[i]] = False
            holes2[ind1[i]] = False

    # We must keep the original values somewhere before scrambling everything
    temp1, temp2 = ind1, ind2
    k1, k2 = b + 1, b + 1
    for i in range(size):
        if not holes1[temp1[(i + b + 1) % size]]:
            ind1[k1 % size] = temp1[(i + b + 1) % size]
            k1 += 1

        if not holes2[temp2[(i + b + 1) % size]]:
            ind2[k2 % size] = temp2[(i + b + 1) % size]
            k2 += 1

    # Swap the content between a and b (included)
    for i in range(a, b + 1):
        ind1[i], ind2[i] = ind2[i], ind1[i]

    return ind1, ind2

# def mpda_PMX():
#     pass

if __name__ == '__main__':
    ind1 = [0, 1, 2, 3, 4]
    ind2 = [4, 3, 2, 1, 0]
    print(tools.cxOrdered(ind1,ind2))

