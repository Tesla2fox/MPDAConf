import  random
import deap
from deap import base
from deap import creator
from deap import tools



IND_ROBNUM = 0
IND_TASKNUM = 0
TOOLBOX = object
LS_NUM = 10
LS_STEP = 2

def mpda_swap_LS(ind):
    lsIndLst = []
    for lsID in range(LS_NUM):
        lsIndLst.append(TOOLBOX.clone(ind))
    for lsInd in lsIndLst:
        r_step = random.randint(1,LS_STEP)
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
    index1 = perm.index(unit1)
    index2 = perm.index(unit2)
    perm[index1] = unit2
    perm[index2] = unit1
    return perm

def mpda_insert_LS(ind):
    lsIndLst = []
    for lsID in range(LS_NUM):
        lsIndLst.append(TOOLBOX.clone(ind))
    for lsInd in lsIndLst:
        rdRobID = random.randint(0,IND_ROBNUM - 1)
        perm = lsInd[(rdRobID * IND_TASKNUM): (rdRobID * IND_TASKNUM + IND_TASKNUM)]
        perm = singleInsert(perm)
        lsInd[(rdRobID * IND_TASKNUM): (rdRobID * IND_TASKNUM + IND_TASKNUM)] = perm
    return lsIndLst



def mpda_v_insert_LS(ind):
    lsIndLst = []
    for lsID in range(LS_NUM):
        lsIndLst.append(TOOLBOX.clone(ind))
    for lsInd in lsIndLst:
        rdRobID = random.randint(0,IND_ROBNUM - 1)
        perm = lsInd.actionSeq.convert2Perm(rdRobID)
        perm = singleInsert(perm)
        realPerm = lsInd[(rdRobID * IND_TASKNUM): (rdRobID * IND_TASKNUM + IND_TASKNUM)]
        permInd = 0
        for i,unit in enumerate(realPerm):
            if unit in perm:
                realPerm[i]  = perm[permInd]
                permInd += 1
        lsInd[(rdRobID * IND_TASKNUM): (rdRobID * IND_TASKNUM + IND_TASKNUM)] = realPerm
    return lsIndLst

def singleInsert(perm):
    if len(perm) == 1:
        return perm
    r_pos1 = random.randint(0, len(perm) - 1)
    element = perm[r_pos1]
    perm.remove(perm[r_pos1])
    r_pos2 = random.randint(0, len(perm) - 1)
    if r_pos2 >= r_pos1:
        r_pos2 += 1
    perm.insert(r_pos2, element)
    return perm


def permutationSinglePointSwap(perm):
    unit1,unit2 = random.sample(perm, 2)
    index1 = perm.index(unit1)
    index2 = perm.index(unit2)
    perm[index1] = unit2
    perm[index2] = unit1
    return perm


def mpda_tri_swap_LS(ind):
    if len(ind.actionSeq._arrCmpltTaskLst) == 0:
        return mpda_swap_LS(ind)
    else:
        robID, taskID = ind.actionSeq._arrCmpltTaskLst[0]
        perm = ind[(robID * IND_TASKNUM): (robID * IND_TASKNUM + IND_TASKNUM)]
        for i in range(perm.index(taskID),IND_TASKNUM - 1):
            perm[i] = perm[i + 1]
        perm[-1] = taskID
        # print(ind[(robID * IND_TASKNUM): (robID * IND_TASKNUM + IND_TASKNUM)])
        ind[(robID * IND_TASKNUM): (robID * IND_TASKNUM + IND_TASKNUM)] =  perm
        return [ind]

def mpda_triangle_LS(ind):
    if len(ind.actionSeq._arrCmpltTaskLst) == 0:
        return []
    else:
        robID, taskID = ind.actionSeq._arrCmpltTaskLst[0]
        perm = ind[(robID * IND_TASKNUM): (robID * IND_TASKNUM + IND_TASKNUM)]
        for i in range(perm.index(taskID),IND_TASKNUM - 1):
            perm[i] = perm[i + 1]
        perm[-1] = taskID
        # print(ind[(robID * IND_TASKNUM): (robID * IND_TASKNUM + IND_TASKNUM)])
        ind[(robID * IND_TASKNUM): (robID * IND_TASKNUM + IND_TASKNUM)] =  perm
        return [ind]