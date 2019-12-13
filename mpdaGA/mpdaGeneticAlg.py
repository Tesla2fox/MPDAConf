
from enum import Enum
import mpdaGA.mpdaMutate as _mutate
import mpdaGA.mpdaCrossover as _crossover
import  mpdaGA.mpdaGAEval as _eval
import mpdaGA.mpdaGAInit as _init

from mpdaInstance import  MPDAInstance
from mpdaDecodeMethod.mpdaDecode import MPDADecoder

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
    def __init__(self,ins : MPDAInstance):

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
        _eval.ga_eval_mpda = MPDADecoder(ins)

        '''
        deap init
        '''
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, typecode='i', fitness=creator.FitnessMin)



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
        self.toolbox.register("select", tools.selTournament,tournsize = 3)

        pass
    def run(self):


        random.seed(1)
        NP = 200
        NGEN = 300
        CXPB, MUTPB = 0.5, 0.3
        pop = self.toolbox.population(n = NP)

        # print(len(pop))
        # exit()
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        fitnesses = map(self.toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        record = stats.compile(pop)
        logbook.record(gen=0, evals=len(pop), **record)
        print(logbook.stream)

        for g in range(1, NGEN + 1):

            offspring = []
            for _ in range(100):
                op_choice = random.random()
                if op_choice < CXPB:  # Apply crossover
                    ind1, ind2 = map(self.toolbox.clone, random.sample(pop, 2))
                    ind1, ind2 = self.toolbox.mate(ind1, ind2)
                    del ind1.fitness.values
                    offspring.append(ind1)
                elif op_choice < CXPB + MUTPB:  # Apply mutation
                    ind = self.toolbox.clone(random.choice(pop))
                    ind, = self.toolbox.mutate(ind)
                    del ind.fitness.values
                    offspring.append(ind)
                else:  # Apply reproduction
                    pass
                    # offspring.append(random.choice(pop))


            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            # print("  Evaluated %i individuals" % len(invalid_ind))
            # Select the next generation population
            pop[:] = self.toolbox.select(pop + offspring, NP)

            hof.update(pop)
            record = stats.compile(pop)
            logbook.record(gen=g, evals=len(pop), **record)
            print(logbook.stream)
            # pop[:] = offspring
            # print(len(pop))
            # exit()

        print('hof = ', hof)
        print("Best individual is ", hof[0], hof[0].fitness.values[0])
        pass


    def __str__(self):
        return 'mpda_ga_opt'

if __name__ == '__main__':

    ins = MPDAInstance()
    insFileName = BaseDir +'//benchmark//8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins.dat'
    ins.loadCfg(fileName =  insFileName)
    mpda_ga = MPDA_Genetic_Alg(ins)

    mpda_ga.run()

    print('main')





