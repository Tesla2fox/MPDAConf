
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

from deap import base
from deap import creator
from deap import tools
import numpy
import random

import os

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
                 reStart = '_NORE',
                 saveData = None, rdSeed = 1):

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
        _eval.ga_eval_mpda = MPDADecoder(ins)
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
        self.toolbox.register("select", _select.selRoulette)
        self.toolbox.register("select",tools.selTournament, tournsize = 3)
            # ()
            #                   tools.selTournament,tournsize = 3)

        if localSearch == '_None':
            self._localSearchBoolean = False
            self._algName += localSearch
        elif localSearch == '_SWAP':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_swap_LS)
            self._algName += localSearch
            self._LSP = 0.7
            _local.TOOLBOX = self.toolbox
        elif localSearch == '_TRI':
            self._localSearchBoolean = True
            self.toolbox.register("localSearch",_local.mpda_triangle_LS)
            self._algName += localSearch
            self._LSP = 1
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

    def run(self):

        randomSeed = self.rdSeed
        random.seed(randomSeed)

        f_con = open(BaseDir + '//debugData//'+str(self.benchmarkName)+ '//'+ str(self._algName) +'//'+ 'r_' + str(randomSeed) + '.dat','w')
        save_data = BaseDir + '//debugData//'+str(self.benchmarkName)+ '//'+ str(self._algName) +'//'+ 'r_' + str(randomSeed) + '.dat'
        print(save_data)

        NP = 300
        NGEN = int(30E4)
        CXPB, MUTPB = 0.5, 0.3

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
            for _ in range(100):
                op_choice = random.random()
                if op_choice < CXPB:  # Apply crossover
                    ind1, ind2 = map(self.toolbox.clone, random.sample(pop, 2))
                    ind1, ind2 = self.toolbox.mate(ind1, ind2)
                    del ind1.fitness.values
                    del ind1.actionSeq
                    offspring.append(ind1)
                elif op_choice < CXPB + MUTPB:  # Apply mutation
                    ind = self.toolbox.clone(random.choice(pop))
                    ind, = self.toolbox.mutate(ind)
                    del ind.fitness.values
                    del ind.actionSeq
                    offspring.append(ind)
                else:  # Apply reproduction
                    pass
                    # offspring.append(random.choice(pop))
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            NFE += len(invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ms, act_seq = fit
                ind.fitness.values = (ms,)
                ind.actionSeq = act_seq
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
            if self._localSearchBoolean:
                for i,ind in enumerate(pop):
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

                                pop[i] = minlInd
                                # print(ind)
                                # exit()
                                # print(len(lIndLst))
                                VLSNFE += len(lIndLst)
                                # print(VLSNFE)
                            NFE += len(lIndLst)
                            LSNFE += len(lIndLst)
            record = stats.compile(pop)
            logbook.record(gen=g, **record)
            print(logbook.stream)
            self.writeDir(f_con, record, g, NFE = NFE)
            VLSNFELST.append(VLSNFE - VLSNFELST[-1])
            # print(logbook.select('gen'))
            # print(logbook.select('min'))
            # exit()
            if NFE > 30E4:
                break
            if self._reStartBoolean:
                # print(record)
                # exit()
                if g <= 10:
                    continue
                minLst = logbook.select('min')
                # print(minLst)
                # print(minLst[-11:])
                if(len(set(minLst[-11:]))==1):
                    print('restart   ==== ')
                    _nfe,pop = self.toolbox.reStart(pop)
                    print('xxx')
                    fitnesses = map(self.toolbox.evaluate, pop)
                    NFE += _nfe
                    for ind, fit in zip(pop, fitnesses):
                        ms, act_seq = fit
                        ind.fitness.values = (ms,)
                        ind.actionSeq = act_seq
                else:
                    pass
        print('hof = ', hof)
        print("Best individual is ", hof[0], hof[0].fitness.values[0])
        print('NFE = ', NFE)
        print('LSNFE = ', LSNFE)
        print('VLSNFE = ', VLSNFE)
        # f_con.write(hof)
        f_con.write(str(hof[0]) + '\n')
        f_con.write('min  '+ str(hof[0].fitness.values[0]) + '\n')
        f_con.write('NFE '+ str(NFE)+ '\n')
        f_con.write('LSNFE '+ str(LSNFE)+ '\n')
        f_con.write('VLSNFE '+ str(VLSNFE)+ '\n')
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





