import os
import sys

'''
'''
# AbsolutePath = os.path.abspath(__file__)
# SuperiorCatalogue = os.path.dirname(AbsolutePath)
# BaseDir = os.path.dirname(SuperiorCatalogue)
# if BaseDir in sys.path:
# #    print('have been added')
#     pass
# else:
#     sys.path.append(BaseDir)
# print(sys.path)
# exit()

from mpdaGA.mpdaGeneticAlg import MPDA_Genetic_Alg, MPDAInstance
from cmpEDA.EDA import MPDA_EDA

if __name__ == '__main__':
    print('begin to run \n')
    ins = MPDAInstance()
    insConfDir = './/benchmark//'
    print(sys.argv)
    print(len(sys.argv))
    if len(sys.argv)== 3:
        benchmarkName = sys.argv[1]
        randomSeed = int(sys.argv[2])
    elif len(sys.argv) == 1:
        benchmarkName = '8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins'
        # benchmarkName = '20_18_RANDOM_ECCENTRIC_QUADRANT_SVLCV_thre0.1MPDAins'
        randomSeed = 1
        localSearch = '_None'
        # localSearch = '_TRI'
        localSearch = '_SWAP'
        # reStart = '_REGEN'
        reStart = '_ELRE'
        # reStart = '_PREGEN'
        # decodeMethod = '_DTRI'
        # decodeMethod = '_NB'
        decodeMethod = '_NONE'
        # reStart = '_NORE'
    else:
        raise Exception('something wrong on the sys.argv')
        pass
    # else:
    #
    #     raise Exception('xxx')
    ins.loadCfg(fileName=insConfDir + benchmarkName + '.dat')
    print(benchmarkName)
    mpda_eda = MPDA_EDA(ins, benchmarkName = benchmarkName, rdSeed= randomSeed)
    # mpda_ga = MPDA_Genetic_Alg(ins, benchmarkName=benchmarkName,
    #                            localSearch=localSearch,
    #                            reStart=reStart, decodeMethod=decodeMethod,
    #                            rdSeed=randomSeed)
    # print(mpda_ga)
    mpda_eda.run()
