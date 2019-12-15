import  random
import deap
from deap import base
from deap import creator
from deap import tools



IND_ROBNUM = 0
IND_TASKNUM = 0
TOOLBOX = object

def mpda_insertion_LS(ind):

    # map(tools.clone,ind)
    lsIndLst = []
    for lsID in range(10):
        lsIndLst.append(TOOLBOX.clone(ind))
    # for x in lsIndLst:
    #     print(x)
    # print('xxx')
    for lsInd in lsIndLst:
        r_step = random.randint(1,2)
        r_stepLst = random.sample(list(range(IND_ROBNUM)),r_step)
        # print(r_stepLst)

        for rdRobID in r_stepLst:
            # rdRobID = random.randint(0, IND_ROBNUM - 1)
            # print(rdRobID)
            perm = lsInd[(rdRobID * IND_TASKNUM) : (rdRobID * IND_TASKNUM + IND_TASKNUM)]
            # print(perm)
            perm  = permutationSinglePointSwap(perm)
            lsInd[(rdRobID * IND_TASKNUM) : (rdRobID * IND_TASKNUM + IND_TASKNUM)] = perm

    return lsIndLst

def permutationSinglePointSwap(perm):
    unit1,unit2 = random.sample(perm, 2)
    # print(unit1,unit2)
    index1 = perm.index(unit1)
    index2 = perm.index(unit2)
    perm[index1] = unit2
    perm[index2] = unit1
    return perm