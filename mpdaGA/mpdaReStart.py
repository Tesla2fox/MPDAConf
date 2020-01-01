import  random
import deap
from deap import base
from deap import creator
from deap import tools
from operator import attrgetter
import mpdaGA.mpdaMutate as _mutate

IND_ROBNUM = 0
IND_TASKNUM = 0
TOOLBOX = object
LS_NUM = 10
LS_STEP = 2


def mpda_regenerate(pop):
    np = len(pop)
    pop = TOOLBOX.population(np)
    NFE = np
    return NFE,pop

def mpda_particalRegenerate(pop):
    np = len(pop)
    NFE = 0
    for i in range(np):
        if random.random() < 0.5:
            pop[i] = TOOLBOX.individual()
            NFE += 1
    return NFE,pop

def mpda_eliteRegenerate(pop):
    s_inds = sorted(pop, key=attrgetter('fitness'), reverse=True)
    np = len(pop)
    NFE = np
    # rPop = []
    for i in range(np):
        if random.random() < 0.9:
            pop[i] = TOOLBOX.individual()
            NFE += 1
        else:
            ind, = _mutate.mpda_mutate(pop[i], 0.1)
            pop[i] = ind
    return NFE,pop


