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

from mpdaGA.mpdaGeneticAlg import  MPDA_Genetic_Alg,MPDAInstance
if __name__ == '__main__':
    print('begin to run \n')
    ins = MPDAInstance()
    insConfDir = './/benchmark//'
    print(sys.argv)
    print(len(sys.argv))
    
    if len(sys.argv)  == 5:
        benchmarkName = sys.argv[1]
        randomSeed = int(sys.argv[2])
        localSearch = sys.argv[3]
        reStart = sys.argv[4]
    elif len(sys.argv) == 1:
        benchmarkName = '8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins'
        randomSeed = 1
        localSearch = '_TRI'
        localSearch = '_SWAP'
        reStart = '_REGEN'
        reStart = '_PREGEN'
    else :
        raise Exception('something wrong on the sys.argv')
        pass
    # else:
    #
    #     raise Exception('xxx')
    localSearchLst = ['_None','_SWAP','_INSERT','_TRI','_VINSERT','_DIST']
    reStartLst = ['_NORE','_REGEN','_PREGEN']
    if localSearch not in localSearchLst:
        print(localSearch)
        raise  Exception('not in the localSearchLst')
    if reStart not in reStartLst:
        print(reStart)
        raise  Exception('not in the reStartLst')
    print(sys.argv)
    ins.loadCfg(fileName=insConfDir + benchmarkName + '.dat')
    print(benchmarkName)
    mpda_ga = MPDA_Genetic_Alg(ins, benchmarkName = benchmarkName ,
                               localSearch = localSearch,
                               reStart = reStart,
                               rdSeed = randomSeed)
    print(mpda_ga)
    mpda_ga.run()
