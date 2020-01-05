#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import random
import math
import numpy as np
from sklearn.cluster import KMeans
from scipy.optimize import curve_fit

from mpdaInstance import  MPDAInstance
from mpdaDecodeMethod.mpdaDecode import MPDADecoder
from mpdaDecodeMethod.mpdaDecoderActSeq import  ActionSeq
import  mpdaGA.mpdaGAEval as _eval
import mpdaGA.mpdaGAInit as _init

from MPDA_decode.MPDA_decode_discrete import  MPDA_Decode_Discrete_RC,MPDA_Decode_Discrete_Base,MPDA_Decode_Discrete_NB

from deap import base
from deap import creator
from deap import tools
import numpy
import random
import time

import os

AbsolutePath = os.path.abspath(__file__)
SuperiorCatalogue = os.path.dirname(AbsolutePath)
BaseDir = os.path.dirname(SuperiorCatalogue)

# import plotly.io as pio

from operator import attrgetter

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, typecode='i', fitness=creator.FitnessMin, actionSeq=object)


class MPDA_EDA(object):
    def __init__(self, ins: MPDAInstance):
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

        self._algName = 'eda_opt_'
        self._algName = 'ga_opt_'


        _eval.IND_ROBNUM = self._robNum
        _eval.IND_TASKNUM = self._taskNum

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, typecode='i', fitness = creator.FitnessMin, actionSeq = object)

        self.toolbox = base.Toolbox()
        self.toolbox.register("mpda_attr", _init.mpda_init_encode, self._robNum, self._taskNum)
        self.toolbox.register("individual", tools.initIterate, creator.Individual,
                         self.toolbox.mpda_attr)

        # define the population to be a list of individuals
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        MPDA_Decode_Discrete_RC._ins = self._ins
        MPDA_Decode_Discrete_Base._ins = self._ins
        _eval.ga_eval_mpda = MPDA_Decode_Discrete_RC()
        self.toolbox.register("evaluate", _eval.mpda_eval_discrete_rc)

        self.toolbox.register("selection", self.selection)
        # self._algName += decodeMethod

        # self.maxIter = int(1e4)
        # self.pop = []
        # #         child pop
        # self.c_pop = []
        # self.popFitness = []

    def generate(self):
        pass
    def selection(self,pop,modelSize):
        s_pop  = sorted(pop, key=attrgetter('fitness'), reverse=True)
        r_pop = []
        for ind in s_pop:
            r_pop.append(ind)
            if len(r_pop) >= modelSize:
                break
        return r_pop
    def statistic(self, s_lst = []):
        self.sMatLst = []
        for i in range(self._robNum):
            mat = np.zeros((self._taskNum, self._taskNum), dtype=int)
            self.sMatLst.append(mat)
        #        print(sMatLst)
        for i in range(self._robNum):
            sMat = self.sMatLst[i]
            # for ind in s_lst:
            #     print(ind)
            #     exit()
                # for in range()
            # raise Exception('xx')
            # for ind in s_lst:
                # robEncode =
            for ind in s_lst:
                # robEncode = self.pop[index][i]
                for robID in range(self._robNum):
                    for pos in range(self._taskNum):
                        taskID = ind[robID * self._taskNum + pos]
                        sMat[pos][taskID] +=1
                        # robEncode[]
        # print(self.sMatLst)
        # exit()

    def model(self,modelSize):
        self.modelLst = []
        for robInd in range(self._robNum):
            robModel = []
            for taskPos in range(self._taskNum):
                #                print('robId = ',robInd, 'taskPos',taskPos)
                data = []
                for i in range(self._taskNum):
                    data.append([i, self.sMatLst[robInd][taskPos][i]])
                kmeans = KMeans(n_clusters=2)
                kmeans.fit(data)
                y_kmeans = kmeans.predict(data)
                poptLst = []
                for i in range(2):
                    x_lst = []
                    y_lst = []
                    for x, setInd in enumerate(y_kmeans):
                        if setInd == i:
                            x_lst.append(x)
                            y_lst.append(data[x][1])
                    x_lst = np.array(x_lst)
                    y_lst = np.array(y_lst)
                    mean = sum(x_lst * y_lst) / sum(y_lst)
                    sigma = np.sqrt(sum(y_lst * (x_lst - mean) ** 2) / sum(y_lst))
                    try:
                        popt, pcov = curve_fit(Gauss, x_lst, y_lst, p0=[max(y_lst), mean, sigma], maxfev=3500)
                    except:
                        popt = [max(y_lst), mean, sigma]
                    ratio = sum(y_lst) / modelSize
                    poptLst.append((ratio, popt))
                robModel.append(tuple(poptLst))
            self.modelLst.append(robModel)

    def sample(self):

        while len(self.c_pop) < self.NP:
            sampleMat = np.zeros((self.robNum, self.taskNum))
            for robInd in range(self.robNum):
                for taskPos in range(self.taskNum):
                    robModel = self.modelLst[robInd][taskPos]
                    popt = []
                    if random.random() < robModel[0][0]:
                        popt = robModel[0][1]
                    else:
                        popt = robModel[1][1]
                    x = random.normalvariate(popt[1], popt[2])
                    sampleMat[robInd][taskPos] = x
            #        sampleMat 2 the encode mat
            encodeMat = np.zeros((self.robNum, self.taskNum), dtype=int)
            for robInd in range(self.robNum):
                enumPerm = list(enumerate(sampleMat[robInd][:]))
                #             print()
                enumPerm = sorted(enumPerm, key=lambda x: x[1])
                #                 print(enumPerm)
                encodeMat[robInd][:] = [x[0] for x in enumPerm]
            #            print(encodeMat)
            self.c_pop.append(encodeMat)
                # for pos in range(len(robEncode)):
                #     taskID = robEncode[pos]
                #     sMat[pos][taskID] += 1
        # if s_pop
    def run(self):

        NP = 300
        modelSize = 300 * 0.3
        ngen = int(1e4)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        logbook = tools.Logbook()
        logbook.header = "gen", "min", "std", "avg", "max"
        # logbook = tools.Logbook()
        # logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        pop = self.toolbox.population(n = NP)
        NFE = 0
        fitnesses = map(self.toolbox.evaluate, pop)
        NFE += len(pop)
        for ind, fit in zip(pop, fitnesses):
            ms,act_seq = fit
            ind.fitness.values = (ms,)
            ind.actionSeq = act_seq
        print('xxx')
        for gen in range(ngen):

            s_lst = self.toolbox.selection(pop,modelSize = modelSize)
            self.statistic(s_lst)
            self.model(modelSize = modelSize)

            # Generate a new population
            # population = self.toolbox.generate()
            # # Evaluate the individuals
            #
            # fitnesses = map(self.toolbox.evaluate, pop)
            # NFE += len(pop)
            # for ind, fit in zip(pop, fitnesses):
            #     ms, act_seq = fit
            #     ind.fitness.values = (ms,)
            #     ind.actionSeq = act_seq
            #
            # fitnesses = self.toolbox.map(toolbox.evaluate, population)
            # for ind, fit in zip(population, fitnesses):
            #     ind.fitness.values = fit
            #
            # if halloffame is not None:
            #     halloffame.update(population)
            #
            # # Update the strategy with the evaluated individuals
            # toolbox.update(population)
            #
            # record = stats.compile(population) if stats is not None else {}
            # logbook.record(gen=gen, nevals=len(population), **record)
            # if verbose:
            #     print(logbook.stream)


# creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMin)


# class EMNA(object):
#     """Estimation of Multivariate Normal Algorithm (EMNA) as described
#     by Algorithm 1 in:
#     Fabien Teytaud and Olivier Teytaud. 2009.
#     Why one must use reweighting in estimation of distribution algorithms.
#     In Proceedings of the 11th Annual conference on Genetic and
#     evolutionary computation (GECCO '09). ACM, New York, NY, USA, 453-460.
#     """
#
#     def __init__(self, centroid, sigma, mu, lambda_):
#         self.dim = len(centroid)
#         self.centroid = numpy.array(centroid)
#         self.sigma = numpy.array(sigma)
#         self.lambda_ = lambda_
#         self.mu = mu
#
#     def generate(self, ind_init):
#         # Generate lambda_ individuals and put them into the provided class
#         arz = self.centroid + self.sigma * numpy.random.randn(self.lambda_, self.dim)
#         return list(map(ind_init, arz))
#
#     def update(self, population):
#         # Sort individuals so the best is first
#         sorted_pop = sorted(population, key=attrgetter("fitness"), reverse=True)
#
#         # Compute the average of the mu best individuals
#         z = sorted_pop[:self.mu] - self.centroid
#         avg = numpy.mean(z, axis=0)
#
#         # Adjust variance of the distribution
#         self.sigma = numpy.sqrt(numpy.sum(numpy.sum((z - avg) ** 2, axis=1)) / (self.mu * self.dim))
#         self.centroid = self.centroid + avg
#
#
# def main():
#     N, LAMBDA = 30, 1000
#     MU = int(LAMBDA / 4)
#     strategy = EMNA(centroid=[5.0] * N, sigma=5.0, mu=MU, lambda_=LAMBDA)
#
#     toolbox = base.Toolbox()
#     toolbox.register("evaluate", benchmarks.sphere)
#     toolbox.register("generate", strategy.generate, creator.Individual)
#     toolbox.register("update", strategy.update)
#
#     # Numpy equality function (operators.eq) between two arrays returns the
#     # equality element wise, which raises an exception in the if similar()
#     # check of the hall of fame. Using a different equality function like
#     # numpy.array_equal or numpy.allclose solve this issue.
#     hof = tools.HallOfFame(1, similar=numpy.array_equal)
#     stats = tools.Statistics(lambda ind: ind.fitness.values)
#     stats.register("avg", numpy.mean)
#     stats.register("std", numpy.std)
#     stats.register("min", numpy.min)
#     stats.register("max", numpy.max)
#
#     algorithms.eaGenerateUpdate(toolbox, ngen=150, stats=stats, halloffame=hof)
#
#     return hof[0].fitness.values[0]
#
def Gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma)


if __name__ == "__main__":
    ins = MPDAInstance()
    insFileName = BaseDir +'//benchmark//8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins.dat'
    ins.loadCfg(fileName =  insFileName)
    mpda_eda = MPDA_EDA(ins)
    mpda_eda.run()

    # main()



