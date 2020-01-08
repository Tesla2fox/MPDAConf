
from enum import Enum
import mpdaGA.mpdaMutate as _mutate
import mpdaGA.mpdaCrossover as _crossover
import  mpdaGA.mpdaGAEval as _eval
import mpdaGA.mpdaGAInit as _init
import mpdaGA.mpdaLocalSearch as _local
import mpdaGA.mpdaReStart as _restart
import mpdaGA.mpdaSelect as _select

from mpdaInstance import  MPDAInstance
from mpdaDecodeMethod.mpdaDecode import MPDADecoder
from mpdaDecodeMethod.mpdaDecoderActSeq import  ActionSeq

from MPDA_decode.MPDA_decode_discrete import  MPDA_Decode_Discrete_RC,MPDA_Decode_Discrete_Base,MPDA_Decode_Discrete_NB

from deap import base
from deap import creator
from deap import tools
import numpy
import random
import time

import os
from operator import attrgetter

AbsolutePath = os.path.abspath(__file__)
SuperiorCatalogue = os.path.dirname(AbsolutePath)
BaseDir = os.path.dirname(SuperiorCatalogue)

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class DecoderType(Enum):
    no_back = 1
    back = 2


class MPDA_Genetic_Alg(object):
    def __init__(self,ins : MPDAInstance,benchmarkName,localSearch = None,
                 reStart = '_NORE',decodeMethod = '_NONE',
                 saveData = None, rdSeed = 1,CXPB = 0.5):
        # raise Exception('xx')

        self._ins = ins
        self._robNum = ins._robNum
        self._taskNum = ins._taskNum
            # int(readCfg.getSingleVal('taskNum'))
        self._threhold = ins._threhold
        self._robAbiLst  = ins._robAbiLst
        self._robVelLst = ins._robVelLst
        self._taskStateLst = ins._taskStateLst
        self._taskRateLst = ins._taskRateLst
        self._rob2taskDisMat = ins._rob2taskDisMat
        self._taskDisMat = ins._taskDisMat

        _mutate.IND_ROBNUM = self._robNum
        _mutate.IND_TASKNUM = self._taskNum

        _crossover.IND_ROBNUM = self._robNum
        _crossover.IND_TASKNUM = self._taskNum

        _eval.IND_ROBNUM = self._robNum
        _eval.IND_TASKNUM = self._taskNum

        _local.IND_ROBNUM = self._robNum
        _local.IND_TASKNUM = self._taskNum

        _restart.IND_ROBNUM = self._robNum
        _restart.IND_TASKNUM = self._taskNum

        self.rdSeed = rdSeed
        self.benchmarkName = benchmarkName
        # if decodeMethod == '_DTRI':
        #     MPDA_Decode_Discrete_NB._ins = self._ins
        #     MPDA_Decode_Discrete_Base._ins = self._ins
        #     _eval.ga_eval_mpda = MPDA_Decode_Discrete_NB()
        # else:
        #     _eval.ga_eval_mpda = MPDADecoder(ins)
        '''
        deap init
        '''
        self._algName = 'ga_opt_'

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, typecode='i', fitness = creator.FitnessMin, actionSeq = object)

        self.toolbox = base.Toolbox()
        self.toolbox.register("mpda_attr", _init.mpda_init_encode, self._robNum, self._taskNum)
        self.toolbox.register("individual", tools.initIterate, creator.Individual,
                         self.toolbox.mpda_attr)

        # define the population to be a list of individuals
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # ----------
        # Operator registration
        # ----------
        # register the goal / fitness function
        if decodeMethod == '_DTRI':
            MPDA_Decode_Discrete_RC._ins = self._ins
            MPDA_Decode_Discrete_Base._ins = self._ins
            _eval.ga_eval_mpda = MPDA_Decode_Discrete_RC()
            self.toolbox.register("evaluate",_eval.mpda_eval_discrete_rc)
            self._algName += decodeMethod
        elif decodeMethod == '_NB':
            MPDA_Decode_Discrete_NB._ins = self._ins
            MPDA_Decode_Discrete_Base._ins = self._ins
            _eval.ga_eval_mpda = MPDA_Decode_Discrete_NB()
            self.toolbox.register("evaluate",_eval.mpda_eval_discrete_nb)
            self._algName += decodeMethod
        else:
            _eval.ga_eval_mpda = MPDADecoder(ins)
            self.toolbox.register("evaluate",_eval.mpda_eval)

        # register the crossover operator
        self.toolbox.register("mate", _crossover.mpda_PMX_mate)

        # register a mutation operator with a probability to
        # flip each attribute/gene of 0.05
        self.toolbox.register("mutate", _mutate.mpda_mutate, indpb=0.01)
        # tools.mutShuffleIndexes
        # tools.mutShuffleIndexes()
        # operator for selecting individuals for breeding the next
        # generation: each individual of the current generation
        # is replaced by the 'fittest' (best) of three individuals
        # drawn randomly from the current generation.
        # tools.selAutomaticEpsilonLexicase(), tournsize=3
        # self.toolbox.register("select", _select.selRoulette)
        # self.toolbox.register("select",tools.selTournament, tournsize = 3)
        self.toolbox.register("select",tools.selBest)
            # ()
            #                   tools.selTournament,tournsize = 3)

        self._mutationBool = False
        self._localSearchStr = localSearch
        if localSearch == '_None':
            self._localSearchBoolean = False
            self._algName += localSearch
            self._mutationBool = True
        elif localSearch == '_SWAP':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_swap_LS)
            self._algName += localSearch
            self._LSP = 0.2
            _local.TOOLBOX = self.toolbox
            self._OneStepBool = True
        elif localSearch == '_MOSWAP':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_swap_LS)
            self._algName += localSearch
            self._LSP = 0.2
            _local.TOOLBOX = self.toolbox
            self._OneStepBool = False
        elif localSearch == '_MNSWAP':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_swap_LS)
            self._algName += localSearch
            self._LSP = 0.2
            _local.TOOLBOX = self.toolbox
            self._OneStepBool = False
        elif localSearch == '_MTRI':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_triangle_LS)
            self._algName += localSearch
            # self._LSP = 0.2
            _local.TOOLBOX = self.toolbox
            self._OneStepBool = False
        elif localSearch == '_TRI':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_triangle_LS)
            self._algName += localSearch
            self._LSP = 0.2
            _local.TOOLBOX = self.toolbox
        elif localSearch == '_INSERT':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_insert_LS)
            self._algName += localSearch
            self._LSP = 0.7
            _local.TOOLBOX = self.toolbox
        elif localSearch == '_VINSERT':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_v_insert_LS)
            self._algName += localSearch
            self._LSP = 0.7
            _local.TOOLBOX = self.toolbox
        elif localSearch == '_DIST':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_v_insert_LS)
            self._algName += localSearch
            self._LSP = 0.7
            _local.TOOLBOX = self.toolbox
        elif localSearch == '_TRISWAP':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_tri_swap_LS)
            self._algName += localSearch
            self._LSP = 0.7
            _local.TOOLBOX = self.toolbox
        else:
            raise  Exception('there is no local method')
            pass
        _restart.TOOLBOX = self.toolbox
        if reStart == '_NORE':
            self._reStartBoolean = False
            self._algName += reStart
        elif reStart == '_REGEN':
            self._reStartBoolean = True
            self._algName += reStart
            self.toolbox.register('reStart',_restart.mpda_regenerate)
        elif reStart == '_PREGEN':
            self._reStartBoolean = True
            self._algName += reStart
            self.toolbox.register('reStart',_restart.mpda_particalRegenerate)
        elif reStart == '_ELRE':
            self._reStartBoolean = True
            self._algName += reStart
            self.toolbox.register('reStart',_restart.mpda_eliteRegenerate)
        else:
            raise Exception('there is no restart method')
            pass
        self.CXPB = CXPB
        if self.CXPB == 1.0:
            self.CXPB = int(self.CXPB)
        self._algName += str(self.CXPB)
        # self._algName += self.__class__
    def run(self):

        randomSeed = self.rdSeed
        random.seed(randomSeed)

        f_con = open(BaseDir + '//debugData//'+str(self.benchmarkName)+ '//'+ str(self._algName) +'//'+ 'r_' + str(randomSeed) + '.dat','w')
        save_data = BaseDir + '//debugData//'+str(self.benchmarkName)+ '//'+ str(self._algName) +'//'+ 'r_' + str(randomSeed) + '.dat'
        print(save_data)

        NP = self._robNum * self._taskNum
        MAXNFE = self._robNum * self._taskNum * 500

        NGEN = int(1E4)
        CXPB, MUTPB = self.CXPB, 0.1
        print('NP  =',NP)
        print('MAXNFE = ',MAXNFE)
        print('CXPB = ', self.CXPB)
        start = time.time()

        pop = self.toolbox.population(n = NP)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        logbook = tools.Logbook()
        logbook.header = "gen", "min", "std", "avg", "max"

        NFE = 0
        fitnesses = map(self.toolbox.evaluate, pop)
        NFE += len(pop)
        for ind, fit in zip(pop, fitnesses):
            ms,act_seq = fit
            ind.fitness.values = (ms,)
            ind.actionSeq = act_seq

        if self._reStartBoolean:
            rg  = 0
        record = stats.compile(pop)
        logbook.record(gen=0, **record)
        print(logbook.stream)
        self.writeDir(f_con, record, 0, NFE = NFE)
        # VLSNFELST = []
        LSNFE  = 0
        VLSNFE = 0
        VLSNFELST = [VLSNFE]
        for g in range(1, NGEN + 1):
            offspring = []
            # for ind in pop:
            for _ in range(len(pop) * 3):
                op_choice = random.random()
                if op_choice< CXPB:
                    # ind1 = self.toolbox.clone(pop[i])
                    # random.randint(0,len(pop)-2)
                    ind1, ind2 = map(self.toolbox.clone, random.sample(pop, 2))
                    ind1, ind2 = self.toolbox.mate(ind1, ind2)
                    del ind1.fitness.values
                    del ind1.actionSeq
                    del ind2.fitness.values
                    del ind2.actionSeq
                    if ind1 not in offspring:
                        offspring.append(ind1)
                    else:
                        pass
                        # raise Exception('XXX')
                    if ind2 not in offspring:
                        # pass
                        offspring.append(ind2)
                    else:
                        pass
                        # raise Exception('xxxxs')
            # print(len(offspring))
            if self._mutationBool:
                for _ in range(len(pop) *3):
                    op_choice = random.random()
                    if op_choice < MUTPB:
                        ind = self.toolbox.clone(random.choice(pop))
                        ind, = self.toolbox.mutate(ind)
                        if ind not in offspring:
                            del ind.fitness.values
                            del ind.actionSeq
                            offspring.append(ind)
            # print(len(offspring))
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            NFE += len(invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ms, act_seq = fit
                ind.fitness.values = (ms,)
                ind.actionSeq = act_seq
            if self._localSearchBoolean:
                if self._localSearchStr == '_SWAP':
                    for i,ind in enumerate(offspring):
                        # bf = ind.fitness.values[0]
                        if random.random() < self._LSP:
                            # lInd = self.toolbox.clone(ind)
                            # print(ind)
                            lIndLst = self.toolbox.localSearch(ind)
                            if len(lIndLst) > 0:
                                for lInd in lIndLst:
                                    del lInd.fitness.values
                                    del lInd.actionSeq
                                    ms,act_seq = self.toolbox.evaluate(lInd)
                                    lInd.fitness.values = (ms,)
                                    lInd.actionSeq = act_seq
                                minlInd = min(lIndLst,key = lambda x: x.fitness.values[0])
                                # try:
                                # print(minlInd.fitness.values[0])
                                if minlInd.fitness.values[0] <= ind.fitness.values[0]:
                                    offspring[i] = minlInd
                                    # print(ind)
                                    # exit()
                                    # print(len(lIndLst))
                                    VLSNFE += len(lIndLst)
                                    # print(VLSNFE)
                                NFE += len(lIndLst)
                                LSNFE += len(lIndLst)
                elif self._localSearchStr == '_MOSWAP':
                    s_inds = sorted(offspring, key=attrgetter('fitness'), reverse=True)
                    ind = s_inds[0]
                    ind_ID = offspring.index(ind)
                    if random.random() < self._LSP:
                        # lInd = self.toolbox.clone(ind)
                        # print(ind)
                        while True:
                            lIndLst = self.toolbox.localSearch(ind)
                            if len(lIndLst) > 0:
                                for lInd in lIndLst:
                                    del lInd.fitness.values
                                    del lInd.actionSeq
                                    ms,act_seq = self.toolbox.evaluate(lInd)
                                    lInd.fitness.values = (ms,)
                                    lInd.actionSeq = act_seq
                                minlInd = min(lIndLst,key = lambda x: x.fitness.values[0])
                                # try:
                                # print(minlInd.fitness.values[0])
                                if minlInd.fitness.values[0] < ind.fitness.values[0]:
                                    offspring[ind_ID] = minlInd
                                    # print(ind)
                                    # exit()
                                    # print(len(lIndLst))
                                    VLSNFE += len(lIndLst)
                                else:
                                    break
                                NFE += len(lIndLst)
                                LSNFE += len(lIndLst)
                    for i,ind in enumerate(offspring):
                        # bf = ind.fitness.values[0]
                        if i == ind_ID:
                            continue
                        if random.random() < self._LSP:
                            # lInd = self.toolbox.clone(ind)
                            # print(ind)
                            lIndLst = self.toolbox.localSearch(ind)
                            if len(lIndLst) > 0:
                                for lInd in lIndLst:
                                    del lInd.fitness.values
                                    del lInd.actionSeq
                                    ms,act_seq = self.toolbox.evaluate(lInd)
                                    lInd.fitness.values = (ms,)
                                    lInd.actionSeq = act_seq
                                minlInd = min(lIndLst,key = lambda x: x.fitness.values[0])
                                # try:
                                # print(minlInd.fitness.values[0])
                                if minlInd.fitness.values[0] <= ind.fitness.values[0]:
                                    offspring[i] = minlInd
                                    # print(ind)
                                    # exit()
                                    # print(len(lIndLst))
                                    VLSNFE += len(lIndLst)
                                    # print(VLSNFE)
                                NFE += len(lIndLst)
                                LSNFE += len(lIndLst)
                elif self._localSearchStr == '_MNSWAP':
                    for i,ind in enumerate(offspring):
                        # bf = ind.fitness.values[0]
                        if random.random() < self._LSP:
                            # lInd = self.toolbox.clone(ind)
                            # print(ind)

                            while True:
                                lIndLst = self.toolbox.localSearch(ind)
                                if len(lIndLst) > 0:
                                    for lInd in lIndLst:
                                        del lInd.fitness.values
                                        del lInd.actionSeq
                                        ms, act_seq = self.toolbox.evaluate(lInd)
                                        lInd.fitness.values = (ms,)
                                        lInd.actionSeq = act_seq
                                    minlInd = min(lIndLst, key=lambda x: x.fitness.values[0])
                                    # try:
                                    # print(minlInd.fitness.values[0])
                                    if minlInd.fitness.values[0] < ind.fitness.values[0]:
                                        offspring[i] = minlInd
                                        # print(ind)
                                        # exit()
                                        # print(len(lIndLst))
                                        VLSNFE += len(lIndLst)
                                    else:
                                        break
                                    NFE += len(lIndLst)
                                    LSNFE += len(lIndLst)


            # elif
            # print("  Evaluated %i individuals" % len(invalid_ind))
            # Select the next generation population
            pop[:] = self.toolbox.select(pop + offspring, NP)
            hof.update(pop)
            # for _ in pop:
            #     print(_)
            # print(pop)
            # print('b LS')
            # logbook.record(gen=g, evals=len(pop), **record)
            # print(logbook.stream)
            '''
            local search
            '''
            record = stats.compile(pop)
            logbook.record(gen=g, **record)
            print(logbook.stream)
            self.writeDir(f_con, record, g, NFE = NFE)
            VLSNFELST.append(VLSNFE - VLSNFELST[-1])
            # print(logbook.select('gen'))
            # print(logbook.select('min'))
            # exit()
            if NFE > MAXNFE:
                break
            if self._reStartBoolean:
                # print(record)
                # exit()
                if g <= rg + 10:
                    continue
                minLst = logbook.select('min')
                # print(minLst)
                # print(minLst[-11:])
                if(len(set(minLst[-11:]))==1):
                    print('restart   ==== ')
                    _nfe,pop = self.toolbox.reStart(pop)
                    # print(pop[0])
                    # print('xxx')
                    fitnesses = map(self.toolbox.evaluate, pop)
                    NFE += _nfe
                    for ind, fit in zip(pop, fitnesses):
                        ms, act_seq = fit
                        ind.fitness.values = (ms,)
                        ind.actionSeq = act_seq
                    # exit()
                    rg = g
                    self._reStartBoolean = False
                else:
                    pass
        print('hof = ', hof)
        print("Best individual is ", hof[0], hof[0].fitness.values[0])
        print('NFE = ', NFE)
        print('LSNFE = ', LSNFE)
        print('VLSNFE = ', VLSNFE)
        # print('complete =',hof[0].actionSeq._arrCmpltTaskLst)
        # f_con.write(hof)
        end = time.time()
        runTime = end - start
        print('runTime',runTime)
        f_con.write(str(hof[0]) + '\n')
        f_con.write('min  '+ str(hof[0].fitness.values[0]) + '\n')
        f_con.write('NFE '+ str(NFE)+ '\n')
        f_con.write('LSNFE '+ str(LSNFE)+ '\n')
        f_con.write('VLSNFE '+ str(VLSNFE)+ '\n')
        f_con.write('runTime ' + str(runTime) + '\n')
        f_con.close()
        pass
        # import plotly.graph_objects as go
        # xLst = []
        # yLst = []
        # for x,y in enumerate(VLSNFELST):
        #     xLst.append(x)
        #     yLst.append(y)
        # fig = go.Figure(data = go.Scatter(x= xLst, y =yLst))
        # fig.show()
    def __str__(self):
        return self._algName

    def writeDir(self, f_con, RecordDic, gen, NFE):
        f_con.write('gen '+ str(gen) + ' ')
        f_con.write(str(NFE) + ' ')
        f_con.write(str(RecordDic['avg']) + ' ')
        f_con.write(str(RecordDic['std']) + ' ')
        f_con.write(str(RecordDic['min']) + ' ')
        f_con.write(str(RecordDic['max']) + ' \n')
        f_con.flush()

if __name__ == '__main__':

    ins = MPDAInstance()
    insFileName = BaseDir +'//benchmark//8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins.dat'
    ins.loadCfg(fileName =  insFileName)
    mpda_ga = MPDA_Genetic_Alg(ins, localSearch = '_LDS')
    mpda_ga.run()

    # print('main')





