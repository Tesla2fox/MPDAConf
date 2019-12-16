import os
import sys
AbsolutePath = os.path.abspath(__file__)
SuperiorCatalogue = os.path.dirname(AbsolutePath)
BaseDir = os.path.dirname(SuperiorCatalogue)
if BaseDir in sys.path:
#    print('have been added')
    pass
else:
    sys.path.append(BaseDir)

from mpdaGA.mpdaGeneticAlg import  MPDA_Genetic_Alg,MPDAInstance

if __name__ == '__main__':
    print('begin to run \n')
    ins = MPDAInstance()
    insConfDir = './/benchmark//'

    if len(sys.argv)  == 4:
        benchmarkName = sys.argv[1]
        randomSeed = int(sys.argv[2])
        localSearch = sys.argv[3]
    elif len(sys.argv) == 1:
        benchmarkName = '8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins'
        randomSeed = 1
        localSearch = 'None'
    else:
        raise Exception('xxx')

    print(sys.argv)
    ins.loadCfg(fileName=insConfDir + benchmarkName + '.dat')
    print(benchmarkName)

    mpda_ga = MPDA_Genetic_Alg(ins, localSearch = localSearch, rdSeed = randomSeed)
    print(mpda_ga)
    mpda_ga.run()
    
    # mpda_ga = MPDA_Genetic_Alg(ins)
